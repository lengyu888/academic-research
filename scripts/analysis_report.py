#!/usr/bin/env python3
"""数据分析 → LaTeX 报告自动生成器（v4.0）。

输入: CSV/Excel 数据文件
输出: .tex 分析报告（含图表）→ 可选编译为 PDF

v4.0 更新:
- --figures: 自动生成 matplotlib/seaborn 图表并保存到 figures/ 目录
- 修复 f-string 渲染: 所有 Python 变量在写入 .tex 前完成替换
- 图表自动嵌入 LaTeX: \\includegraphics + \\graphicspath

用法:
  python analysis_report.py data.csv                                # 纯 .tex（无图）
  python analysis_report.py data.csv --figures                      # .tex + 图表
  python analysis_report.py data.csv --figures --compile            # .tex + 图表 + PDF
  python analysis_report.py data.csv --figures --compile --group-col model
"""

import csv
import math
import os
import sys
from datetime import datetime


# ── CSV 加载 ──────────────────────────────────────────────────────

def load_csv(filepath: str, encoding: str = 'utf-8') -> tuple:
    """加载 CSV，返回 (header, rows)。自动检测编码。"""
    for enc in [encoding, 'utf-8', 'gbk', 'gb2312', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = [row for row in reader]
            return header, rows
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode {filepath}")


# ── 统计工具 ──────────────────────────────────────────────────────

def col_is_numeric(values: list) -> bool:
    n = sum(1 for v in values if _try_float(v) is not None)
    return n / max(len(values), 1) > 0.85


def _try_float(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def as_floats(values: list) -> list:
    return [x for v in values if (x := _try_float(v)) is not None]


def percentile(sorted_data: list, p: float) -> float:
    k = (len(sorted_data) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)


def calc_stats(nums: list) -> dict:
    n = len(nums)
    if n == 0:
        return {'N': 0, 'Mean': 0, 'SD': 0, 'Min': 0, 'Q1': 0, 'Median': 0, 'Q3': 0, 'Max': 0}
    if n == 1:
        return {'N': 1, 'Mean': round(nums[0], 4), 'SD': 0, 'Min': nums[0], 'Q1': nums[0],
                'Median': nums[0], 'Q3': nums[0], 'Max': nums[0]}
    m = sum(nums) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in nums) / (n - 1))
    s = sorted(nums)
    return {
        'N': n, 'Mean': round(m, 4), 'SD': round(sd, 4),
        'Min': round(s[0], 4), 'Q1': round(percentile(s, 0.25), 4),
        'Median': round(percentile(s, 0.50), 4), 'Q3': round(percentile(s, 0.75), 4),
        'Max': round(s[-1], 4),
    }


def iqr_outliers(nums: list) -> int:
    if len(nums) < 4:
        return 0
    s = sorted(nums)
    q1, q3 = percentile(s, 0.25), percentile(s, 0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return sum(1 for x in nums if x < lo or x > hi)


# ── LaTeX 转义 ────────────────────────────────────────────────────

def tex_escape(s: str) -> str:
    return s.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('#', r'\#')


# ── 图表生成 ──────────────────────────────────────────────────────

def generate_figures(report: dict, fig_dir: str):
    """生成 matplotlib 图表并保存到 fig_dir。"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
    except ImportError:
        print("[WARN] matplotlib not installed, skipping figures", file=sys.stderr)
        return []

    # 尝试设置中文字体
    for font_name in ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'Arial Unicode MS']:
        try:
            fm.findfont(font_name, fallback_to_default=False)
            plt.rcParams['font.sans-serif'] = [font_name]
            break
        except Exception:
            continue
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.bbox'] = 'tight'

    os.makedirs(fig_dir, exist_ok=True)
    fig_files = []
    num_stats = report.get('num_stats', {})
    group_comparisons = report.get('group_comparisons', {})
    columns = report.get('columns', {})
    numeric_cols = list(num_stats.keys())

    if not numeric_cols:
        return fig_files

    # ── Fig 1: 各数值变量箱线图 ──
    try:
        fig, axes = plt.subplots(1, min(len(numeric_cols), 4), figsize=(4 * min(len(numeric_cols), 4), 4))
        if not hasattr(axes, '__iter__'):
            axes = [axes]
        for i, col in enumerate(numeric_cols[:4]):
            data = as_floats(columns.get(col, []))
            if data:
                axes[i].boxplot(data, tick_labels=[col])
                axes[i].set_title(col, fontsize=10)
                axes[i].tick_params(labelsize=8)
        plt.tight_layout()
        path = os.path.join(fig_dir, 'fig1_boxplots.png')
        plt.savefig(path)
        plt.close()
        fig_files.append('fig1_boxplots.png')
    except Exception as e:
        print(f"[WARN] Fig1 failed: {e}", file=sys.stderr)
        plt.close('all')

    # ── Fig 2: 分组对比柱状图（如果有分组变量）──
    for label, group_stats in group_comparisons.items():
        try:
            groups = list(group_stats.keys())
            if len(groups) < 2:
                continue
            # 取第一个数值变量做对比
            first_col = numeric_cols[0]
            means = [group_stats[g].get(first_col, {}).get('Mean', 0) for g in groups]
            sds = [group_stats[g].get(first_col, {}).get('SD', 0) for g in groups]

            fig, ax = plt.subplots(figsize=(max(6, len(groups) * 1.5), 4))
            x_pos = range(len(groups))
            bars = ax.bar(x_pos, means, yerr=sds, capsize=4, color='steelblue', alpha=0.8, edgecolor='navy')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(groups, rotation=30, ha='right', fontsize=9)
            ax.set_ylabel(first_col, fontsize=10)
            ax.set_title(f'{first_col} by {label}', fontsize=11)
            # 在柱子上方标注均值
            for bar, m in zip(bars, means):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                        f'{m:.3f}', ha='center', va='bottom', fontsize=8)
            plt.tight_layout()
            path = os.path.join(fig_dir, 'fig2_group_comparison.png')
            plt.savefig(path)
            plt.close()
            fig_files.append('fig2_group_comparison.png')
            break  # 只为第一个分组变量生成
        except Exception as e:
            print(f"[WARN] Fig2 failed: {e}", file=sys.stderr)
            plt.close('all')

    # ── Fig 3: 多变量相关性热力图 ──
    if len(numeric_cols) >= 2:
        try:
            import numpy as np
            # 计算相关系数矩阵
            data_matrix = []
            for col in numeric_cols:
                data_matrix.append(as_floats(columns.get(col, [])))
            # 对齐长度
            min_len = min(len(d) for d in data_matrix)
            data_matrix = [d[:min_len] for d in data_matrix]
            n_vars = len(data_matrix)
            corr = np.zeros((n_vars, n_vars))
            for i in range(n_vars):
                for j in range(n_vars):
                    if i == j:
                        corr[i][j] = 1.0
                    else:
                        mi = sum(data_matrix[i]) / min_len
                        mj = sum(data_matrix[j]) / min_len
                        num = sum((data_matrix[i][k] - mi) * (data_matrix[j][k] - mj) for k in range(min_len))
                        di = math.sqrt(sum((data_matrix[i][k] - mi) ** 2 for k in range(min_len)))
                        dj = math.sqrt(sum((data_matrix[j][k] - mj) ** 2 for k in range(min_len)))
                        corr[i][j] = num / (di * dj) if di > 0 and dj > 0 else 0

            fig, ax = plt.subplots(figsize=(max(5, n_vars * 1.2), max(4, n_vars * 1.0)))
            im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
            ax.set_xticks(range(n_vars))
            ax.set_yticks(range(n_vars))
            ax.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=8)
            ax.set_yticklabels(numeric_cols, fontsize=8)
            for i in range(n_vars):
                for j in range(n_vars):
                    ax.text(j, i, f'{corr[i][j]:.2f}', ha='center', va='center', fontsize=7,
                            color='white' if abs(corr[i][j]) > 0.5 else 'black')
            plt.colorbar(im, ax=ax, shrink=0.8)
            ax.set_title('Correlation Matrix', fontsize=11)
            plt.tight_layout()
            path = os.path.join(fig_dir, 'fig3_correlation.png')
            plt.savefig(path)
            plt.close()
            fig_files.append('fig3_correlation.png')
        except ImportError:
            print("[WARN] numpy not available, skipping correlation heatmap", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Fig3 failed: {e}", file=sys.stderr)
            plt.close('all')

    # ── Fig 4: 分组×变量 交互热力图 ──
    for label, group_stats in group_comparisons.items():
        try:
            groups = list(group_stats.keys())
            if len(groups) < 2 or len(numeric_cols) < 2:
                continue
            # 构建均值矩阵
            matrix = []
            for g in groups:
                row = [group_stats[g].get(c, {}).get('Mean', 0) for c in numeric_cols]
                matrix.append(row)
            import numpy as np
            matrix = np.array(matrix)

            fig, ax = plt.subplots(figsize=(max(6, len(numeric_cols) * 1.5), max(4, len(groups) * 0.8)))
            im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
            ax.set_xticks(range(len(numeric_cols)))
            ax.set_yticks(range(len(groups)))
            ax.set_xticklabels(numeric_cols, rotation=30, ha='right', fontsize=8)
            ax.set_yticklabels(groups, fontsize=9)
            for i in range(len(groups)):
                for j in range(len(numeric_cols)):
                    ax.text(j, i, f'{matrix[i][j]:.3f}', ha='center', va='center', fontsize=8)
            plt.colorbar(im, ax=ax, shrink=0.8)
            ax.set_title(f'Mean Values: {label} x Variables', fontsize=11)
            plt.tight_layout()
            path = os.path.join(fig_dir, 'fig4_interaction.png')
            plt.savefig(path)
            plt.close()
            fig_files.append('fig4_interaction.png')
            break
        except Exception as e:
            print(f"[WARN] Fig4 failed: {e}", file=sys.stderr)
            plt.close('all')

    return fig_files


# ── LaTeX 生成 ────────────────────────────────────────────────────

def build_tex(report: dict, output_path: str, fig_files: list = None):
    """根据报告字典生成 .tex 文件。所有 Python 变量在拼接时完成替换。"""
    fig_files = fig_files or []
    lines = []

    # ── Preamble ──
    lines.append(r'\documentclass[12pt,a4paper]{ctexart}')
    lines.append(r'\usepackage[top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}')
    lines.append(r'\usepackage{amsmath,amssymb}')
    lines.append(r'\usepackage{graphicx}')
    lines.append(r'\usepackage{booktabs}')
    lines.append(r'\usepackage{xcolor}')
    lines.append(r'\usepackage{enumitem}')
    lines.append(r'\usepackage{fancyhdr}')
    lines.append(r'\usepackage{float}')
    lines.append(r'\usepackage{caption}')
    lines.append(r'\pagestyle{fancy}')
    lines.append(r'\fancyhf{}')
    lines.append(r'\fancyhead[R]{\small\textcolor{gray}{数据分析报告}}')
    lines.append(r'\fancyfoot[C]{\thepage}')
    lines.append(r'\renewcommand{\headrulewidth}{0.4pt}')
    if fig_files:
        lines.append(r'\graphicspath{{figures/}}')
    lines.append(r'')
    lines.append(r'\begin{document}')
    lines.append(r'')

    # ── 标题 ──
    title = tex_escape(report.get('title', '数据分析报告'))
    lines.append(r'\title{' + title + r'}')
    lines.append(r'\author{}')
    lines.append(r'\date{' + datetime.now().strftime('%Y-%m-%d') + r'}')
    lines.append(r'\maketitle')
    lines.append(r'')

    # ── 1. 数据概览 ──
    lines.append(r'\section{数据概览}')
    lines.append(r'\begin{itemize}[leftmargin=2em]')
    lines.append(r'  \item 数据文件：' + tex_escape(report.get('file', '')))
    lines.append(r'  \item 样本量：$N = ' + str(report.get('n_rows', 0)) + r'$')
    lines.append(r'  \item 变量数：' + str(report.get('n_cols', 0)) +
                 r'（数值型 ' + str(len(report.get('num_stats', {}))) + r' 个）')
    lines.append(r'\end{itemize}')
    lines.append(r'')

    # ── 2. 描述性统计 ──
    num_stats = report.get('num_stats', {})
    if num_stats:
        lines.append(r'\section{描述性统计}')

        # 汇总表
        lines.append(r'\begin{table}[H]')
        lines.append(r'\centering')
        lines.append(r'\caption{各变量描述性统计汇总}')
        lines.append(r'\label{tab:desc}')
        lines.append(r'\begin{tabular}{lcccccc}')
        lines.append(r'\toprule')
        lines.append(r'变量 & $N$ & $M$ & $SD$ & Min & Max & Median \\')
        lines.append(r'\midrule')
        for col_name, s in num_stats.items():
            row = (tex_escape(col_name) + ' & ' +
                   str(s['N']) + ' & ' +
                   f"{s['Mean']:.4f}" + ' & ' +
                   f"{s['SD']:.4f}" + ' & ' +
                   f"{s['Min']:.4f}" + ' & ' +
                   f"{s['Max']:.4f}" + ' & ' +
                   f"{s['Median']:.4f}" + r' \\')
            lines.append(row)
        lines.append(r'\bottomrule')
        lines.append(r'\end{tabular}')
        lines.append(r'\end{table}')
        lines.append(r'')

        # 每个变量的详细统计表
        for col_name, s in num_stats.items():
            lines.append(r'\subsection{' + tex_escape(col_name) + '}')
            lines.append(r'\begin{table}[H]')
            lines.append(r'\centering')
            lines.append(r'\caption{' + tex_escape(col_name) + r' 详细统计 ($N=' + str(s['N']) + r'$)}')
            lines.append(r'\begin{tabular}{lrlr}')
            lines.append(r'\toprule')
            lines.append(r'指标 & 值 & 指标 & 值 \\')
            lines.append(r'\midrule')
            lines.append(f"Mean & {s['Mean']:.4f} & SD & {s['SD']:.4f} \\\\")
            lines.append(f"Min & {s['Min']:.4f} & Max & {s['Max']:.4f} \\\\")
            lines.append(f"Q1 & {s['Q1']:.4f} & Q3 & {s['Q3']:.4f} \\\\")
            lines.append(f"Median & {s['Median']:.4f} & & \\\\")
            lines.append(r'\bottomrule')
            lines.append(r'\end{tabular}')
            lines.append(r'\end{table}')
            lines.append(r'')

    # ── 3. 分组对比 ──
    for label, group_stats in report.get('group_comparisons', {}).items():
        lines.append(r'\section{分组对比：' + tex_escape(label) + '}')
        groups = list(group_stats.keys())
        all_cols = set()
        for g in groups:
            all_cols.update(group_stats[g].keys())
        all_cols = sorted(all_cols)

        lines.append(r'\begin{table}[H]')
        lines.append(r'\centering')
        lines.append(r'\caption{' + tex_escape(label) + r' 各组均值对比}')
        lines.append(r'\begin{tabular}{l' + 'c' * len(all_cols) + '}')
        lines.append(r'\toprule')
        lines.append(r'组别 & ' + ' & '.join(tex_escape(c) for c in all_cols) + r' \\')
        lines.append(r'\midrule')
        for g in groups:
            vals = []
            for c in all_cols:
                v = group_stats[g].get(c, {})
                if isinstance(v, dict):
                    vals.append(f"{v.get('Mean', 0):.4f}")
                else:
                    vals.append('-')
            lines.append(tex_escape(g) + ' & ' + ' & '.join(vals) + r' \\')
        lines.append(r'\bottomrule')
        lines.append(r'\end{tabular}')
        lines.append(r'\end{table}')
        lines.append(r'')

        # 各组 SD 对比
        lines.append(r'\begin{table}[H]')
        lines.append(r'\centering')
        lines.append(r'\caption{' + tex_escape(label) + r' 各组标准差对比}')
        lines.append(r'\begin{tabular}{l' + 'c' * len(all_cols) + '}')
        lines.append(r'\toprule')
        lines.append(r'组别 & ' + ' & '.join(tex_escape(c) for c in all_cols) + r' \\')
        lines.append(r'\midrule')
        for g in groups:
            vals = []
            for c in all_cols:
                v = group_stats[g].get(c, {})
                if isinstance(v, dict):
                    vals.append(f"{v.get('SD', 0):.4f}")
                else:
                    vals.append('-')
            lines.append(tex_escape(g) + ' & ' + ' & '.join(vals) + r' \\')
        lines.append(r'\bottomrule')
        lines.append(r'\end{tabular}')
        lines.append(r'\end{table}')
        lines.append(r'')

    # ── 4. 异常值 ──
    outliers = report.get('outliers', {})
    if outliers:
        lines.append(r'\section{异常值检测}')
        lines.append(r'采用 IQR 方法检测异常值（$1.5 \times \mathrm{IQR}$ 以外的观测）：')
        lines.append(r'\begin{itemize}[leftmargin=2em]')
        for col_name, count in outliers.items():
            lines.append(r'  \item ' + tex_escape(col_name) + '：' + str(count) + r' 个异常值')
        lines.append(r'\end{itemize}')
        lines.append(r'')

    # ── 5. 可视化 ──
    if fig_files:
        lines.append(r'\section{可视化}')
        fig_captions = {
            'fig1_boxplots.png': '各数值变量箱线图',
            'fig2_group_comparison.png': '分组对比柱状图（误差棒为标准差）',
            'fig3_correlation.png': '变量间相关系数热力图',
            'fig4_interaction.png': '分组 $\times$ 变量均值热力图',
        }
        for fig_file in fig_files:
            caption = fig_captions.get(fig_file, fig_file)
            lines.append(r'\begin{figure}[H]')
            lines.append(r'\centering')
            lines.append(r'\includegraphics[width=0.85\textwidth]{' + fig_file + '}')
            lines.append(r'\caption{' + caption + '}')
            lines.append(r'\end{figure}')
            lines.append(r'')

    # ── 6. 主要发现 ──
    lines.append(r'\section{主要发现}')
    findings = report.get('findings', [])
    lines.append(r'\begin{enumerate}[leftmargin=2em]')
    for finding in findings:
        lines.append(r'  \item ' + tex_escape(finding))
    lines.append(r'\end{enumerate}')
    lines.append(r'')

    lines.append(r'\end{document}')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


# ── 报告构建 ──────────────────────────────────────────────────────

def build_report(filepath: str, group_col: str = None, encoding: str = 'utf-8') -> dict:
    """从 CSV 构建分析报告字典。"""
    header, rows = load_csv(filepath, encoding)
    n_rows = len(rows)
    n_cols = len(header)

    # 按列提取数据
    columns = {}
    for i, col in enumerate(header):
        columns[col] = [row[i] if i < len(row) else '' for row in rows]

    numeric_cols = [c for c in header if col_is_numeric(columns[c])]

    # 数值统计
    num_stats = {}
    for c in numeric_cols:
        nums = as_floats(columns[c])
        num_stats[c] = calc_stats(nums)

    # 异常值
    outliers = {}
    for c in numeric_cols:
        nums = as_floats(columns[c])
        n_out = iqr_outliers(nums)
        if n_out > 0:
            outliers[c] = n_out

    # 分组对比
    group_comparisons = {}
    if group_col and group_col in header:
        gi = header.index(group_col)
        groups = {}
        for row in rows:
            g = row[gi] if gi < len(row) else 'Unknown'
            groups.setdefault(g, {})
            for c in numeric_cols:
                ci = header.index(c)
                val = _try_float(row[ci]) if ci < len(row) else None
                groups[g].setdefault(c, []).append(val if val is not None else 0)
        group_stats = {}
        for g, cols in groups.items():
            group_stats[g] = {c: calc_stats(vals) for c, vals in cols.items()}
        group_comparisons[group_col] = group_stats

    # 自动生成发现
    findings = []
    findings.append(f'共 {n_rows} 条有效记录，{n_cols} 个变量，其中数值型变量 {len(numeric_cols)} 个')

    if num_stats:
        # 找均值最高和最低的变量
        max_col = max(num_stats, key=lambda c: num_stats[c]['Mean'])
        min_col = min(num_stats, key=lambda c: num_stats[c]['Mean'])
        if max_col != min_col:
            findings.append(
                f'均值最高的变量为 {max_col}（$M = {num_stats[max_col]["Mean"]:.4f}$），'
                f'最低为 {min_col}（$M = {num_stats[min_col]["Mean"]:.4f}$）'
            )
        # 找标准差最大的变量
        max_sd_col = max(num_stats, key=lambda c: num_stats[c]['SD'])
        findings.append(f'标准差最大的变量为 {max_sd_col}（$SD = {num_stats[max_sd_col]["SD"]:.4f}$），离散程度最高')

    if outliers:
        total_outliers = sum(outliers.values())
        findings.append(f'共检测到 {total_outliers} 个异常值，涉及 {len(outliers)} 个变量')

    if group_comparisons:
        for label, gs in group_comparisons.items():
            groups = list(gs.keys())
            findings.append(f'分组变量 {label} 包含 {len(groups)} 个组别：{", ".join(groups)}')

    return {
        'title': f'数据分析报告: {os.path.basename(filepath)}',
        'file': os.path.basename(filepath),
        'n_rows': n_rows,
        'n_cols': n_cols,
        'columns': columns,
        'num_stats': num_stats,
        'outliers': outliers,
        'group_comparisons': group_comparisons,
        'findings': findings,
    }


# ── 主函数 ────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate LaTeX analysis report from CSV (v4.0)')
    parser.add_argument('file', help='CSV data file')
    parser.add_argument('--encoding', '-e', default='utf-8', help='CSV encoding')
    parser.add_argument('--output', '-o', help='Output .tex path (default: <file>_report.tex)')
    parser.add_argument('--compile', '-c', action='store_true', help='Also compile to PDF')
    parser.add_argument('--group-col', help='Column name for grouped comparison')
    parser.add_argument('--figures', '-f', action='store_true', help='Generate matplotlib figures')
    parser.add_argument('--fig-dir', help='Figure output directory (default: figures/ alongside .tex)')
    parser.add_argument('--title', help='Report title')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    # 构建报告
    report = build_report(args.file, group_col=args.group_col, encoding=args.encoding)
    if args.title:
        report['title'] = args.title

    out_tex = args.output or os.path.splitext(args.file)[0] + '_report.tex'
    tex_dir = os.path.dirname(os.path.abspath(out_tex))

    # 生成图表
    fig_files = []
    if args.figures:
        fig_dir = args.fig_dir or os.path.join(tex_dir, 'figures')
        fig_files = generate_figures(report, fig_dir)
        if fig_files:
            print(f"[OK] {len(fig_files)} figures saved to {fig_dir}/")

    # 生成 .tex
    build_tex(report, out_tex, fig_files)
    print(f"[OK] TeX generated: {out_tex}")

    # 编译 PDF
    if args.compile:
        import subprocess
        compile_py = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  'references', 'latex', 'scripts', 'compile.py')
        if os.path.exists(compile_py):
            print(f"[INFO] Compiling PDF...")
            result = subprocess.run(['uv', 'run', 'python', compile_py, out_tex], check=False)
            if result.returncode == 0:
                pdf_path = os.path.splitext(out_tex)[0] + '.pdf'
                if os.path.exists(pdf_path):
                    print(f"[OK] PDF generated: {pdf_path}")
                else:
                    print("[WARN] Compilation finished but PDF not found", file=sys.stderr)
            else:
                print(f"[ERROR] Compilation failed with exit code {result.returncode}", file=sys.stderr)
        else:
            print("[WARN] compile.py not found, skipping PDF compilation", file=sys.stderr)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""数据分析 → LaTeX 报告自动生成器。

输入: CSV/Excel 数据文件
输出: .tex 分析报告（可选编译为 PDF）

这是 data-processing 模块的输出管道末端，
遵循 skill 的 PDF 生成流程: .tex → compile.py → .pdf

用法:
  python analysis_report.py data.csv                          # 生成 .tex
  python analysis_report.py data.csv --compile                # 生成 .tex + 编译 PDF
  python analysis_report.py data.csv --model-compare model    # 按 model 分组对比
  python analysis_report.py data.csv --group-col GroupVar     # 指定分组变量
"""

import csv
import math
import os
import sys
from datetime import datetime


def load_csv(filepath: str, encoding: str = 'utf-8') -> tuple[list, list[list]]:
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


def col_is_numeric(values: list) -> bool:
    n = 0
    for v in values:
        try:
            float(v)
            n += 1
        except (ValueError, TypeError):
            pass
    return n / max(len(values), 1) > 0.85


def as_floats(values: list) -> list[float]:
    result = []
    for v in values:
        try:
            result.append(float(v))
        except (ValueError, TypeError):
            pass
    return result


def stats(nums: list[float]) -> dict:
    n = len(nums)
    if n < 2:
        return {'N': n, 'Mean': round(nums[0], 4) if n else 0, 'SD': 0}
    m = sum(nums) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in nums) / (n - 1))
    s = sorted(nums)
    def pct(data, p):
        k = (len(data) - 1) * p
        f, c = math.floor(k), math.ceil(k)
        if f == c:
            return data[int(k)]
        return data[f] * (c - k) + data[c] * (k - f)
    return {
        'N': n, 'Mean': round(m, 4), 'SD': round(sd, 4),
        'Min': round(s[0], 4), 'Q1': round(pct(s, 0.25), 4),
        'Median': round(pct(s, 0.50), 4), 'Q3': round(pct(s, 0.75), 4),
        'Max': round(s[-1], 4),
    }


def tex_escape(s: str) -> str:
    return s.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('#', r'\#')


def build_tex(report: dict, output_path: str):
    """根据报告字典生成 .tex 文件。"""
    lines = []
    lines.append(r'\documentclass[12pt,a4paper]{ctexart}')
    lines.append(r'\usepackage[top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}')
    lines.append(r'\usepackage{amsmath,amssymb}')
    lines.append(r'\usepackage{graphicx}')
    lines.append(r'\usepackage{booktabs}')
    lines.append(r'\usepackage{xcolor}')
    lines.append(r'\usepackage{enumitem}')
    lines.append(r'\usepackage{fancyhdr}')
    lines.append(r'\pagestyle{fancy}')
    lines.append(r'\fancyhf{}')
    lines.append(r'\fancyhead[R]{\small\textcolor{gray}{数据分析报告}}')
    lines.append(r'\fancyfoot[C]{\thepage}')
    lines.append(r'\renewcommand{\headrulewidth}{0.4pt}')
    lines.append(r'')
    lines.append(r'\begin{document}')
    lines.append(r'')
    lines.append(r'\title{' + tex_escape(report.get('title', '数据分析报告')) + r'}')
    lines.append(r'\author{Academic Research Skill}')
    lines.append(r'\date{' + datetime.now().strftime('%Y年%m月%d日') + r'}')
    lines.append(r'\maketitle')
    lines.append(r'')

    # 数据概览
    lines.append(r'\section{数据概览}')
    lines.append(r'\begin{itemize}')
    lines.append(r'  \item 数据文件：' + tex_escape(report.get('file', '')))
    lines.append(r'  \item 样本量：N = ' + str(report.get('n_rows', 0)))
    lines.append(r'  \item 变量数：' + str(report.get('n_cols', 0)))
    lines.append(r'\end{itemize}')
    lines.append(r'')

    # 变量类型
    lines.append(r'\section{变量与描述性统计}')
    for col_name, s in report.get('num_stats', {}).items():
        lines.append(r'\subsection{' + tex_escape(col_name) + r'}')
        lines.append(r'\begin{table}[htbp]')
        lines.append(r'\centering')
        lines.append(r'\caption{' + tex_escape(col_name) + r' 描述性统计 (N=' + str(s.get('N', 0)) + r')}')
        lines.append(r'\begin{tabular}{lrlr}')
        lines.append(r'\toprule')
        lines.append(r'指标 & 值 & 指标 & 值 \\')
        lines.append(r'\midrule')
        lines.append(f"Mean & {s.get('Mean', '')} & SD & {s.get('SD', '')} \\\\")
        lines.append(f"Min & {s.get('Min', '')} & Max & {s.get('Max', '')} \\\\")
        lines.append(f"Q1 & {s.get('Q1', '')} & Q3 & {s.get('Q3', '')} \\\\")
        lines.append(f"Median & {s.get('Median', '')} & & \\\\")
        lines.append(r'\bottomrule')
        lines.append(r'\end{tabular}')
        lines.append(r'\end{table}')
        lines.append(r'')

    # 按分组对比
    for label, group_stats in report.get('group_comparisons', {}).items():
        lines.append(r'\section{分组对比: ' + tex_escape(label) + r'}')
        for group_name, cols in group_stats.items():
            lines.append(r'\subsection{' + tex_escape(group_name) + r'}')
            lines.append(r'\begin{table}[htbp]')
            lines.append(r'\centering')
            lines.append(r'\caption{' + tex_escape(group_name) + r' 各组描述性统计}')
            col_names = list(cols.keys())
            lines.append(r'\begin{tabular}{l' + 'c' * len(col_names) + r'}')
            lines.append(r'\toprule')
            lines.append(r'指标 & ' + ' & '.join(tex_escape(c) for c in col_names) + r' \\')
            lines.append(r'\midrule')
            metrics = ['N', 'Mean', 'SD', 'Min', 'Median', 'Max']
            for metric in metrics:
                vals = [str(cols[c].get(metric, '')) if isinstance(cols[c], dict) else '' for c in col_names]
                lines.append(metric + r' & ' + ' & '.join(vals) + r' \\')
            lines.append(r'\bottomrule')
            lines.append(r'\end{tabular}')
            lines.append(r'\end{table}')
            lines.append(r'')

    # 异常值
    if report.get('outliers'):
        lines.append(r'\section{异常值}')
        lines.append(r'\begin{itemize}')
        for col_name, count in report['outliers'].items():
            lines.append(r'  \item ' + tex_escape(col_name) + '：' + str(count) + ' 个异常值')
        lines.append(r'\end{itemize}')
        lines.append(r'')

    # 结论
    lines.append(r'\section{主要发现}')
    lines.append(r'\begin{enumerate}')
    for finding in report.get('findings', []):
        lines.append(r'  \item ' + tex_escape(finding))
    lines.append(r'\end{enumerate}')
    lines.append(r'')

    lines.append(r'\end{document}')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


def build_report(filepath: str, group_col: str = None, encoding: str = 'utf-8') -> dict:
    """从 CSV 构建分析报告字典。"""
    header, rows = load_csv(filepath, encoding)
    n_rows = len(rows)
    n_cols = len(header)

    columns = {}
    for i, col in enumerate(header):
        columns[col] = [row[i] if i < len(row) else '' for row in rows]

    # 类型推断
    numeric_cols = [c for c in header if col_is_numeric(columns[c])]

    # 数值统计
    num_stats = {}
    for c in numeric_cols:
        nums = as_floats(columns[c])
        num_stats[c] = stats(nums)

    # 异常值检测 (IQR)
    outliers = {}
    for c in numeric_cols:
        nums = as_floats(columns[c])
        s = sorted(nums)
        def pct(data, p):
            k = (len(data) - 1) * p
            f, c = math.floor(k), math.ceil(k)
            return data[f] * (c - k) + data[c] * (k - f) if f != c else data[int(k)]
        q1, q3 = pct(s, 0.25), pct(s, 0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = sum(1 for x in nums if x < lo or x > hi)
        if n_out > 0:
            outliers[c] = n_out

    # 分组对比
    group_comparisons = {}
    if group_col and group_col in columns:
        groups = {}
        for i, row in enumerate(rows):
            g = row[header.index(group_col)]
            groups.setdefault(g, {})
            for c in numeric_cols:
                groups[g].setdefault(c, []).append(float(row[header.index(c)]) if row[header.index(c)] else 0)
        group_stats = {}
        for g, cols in groups.items():
            group_stats[g] = {c: stats(vals) for c, vals in cols.items()}
        group_comparisons[group_col] = group_stats

    return {
        'title': f'数据分析报告: {os.path.basename(filepath)}',
        'file': os.path.basename(filepath),
        'n_rows': n_rows,
        'n_cols': n_cols,
        'num_stats': num_stats,
        'outliers': outliers,
        'group_comparisons': group_comparisons,
        'findings': [
            f'共 {n_rows} 条记录，{n_cols} 个变量，其中数值型 {len(numeric_cols)} 个',
            '详见描述性统计表格',
        ],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate LaTeX analysis report from CSV')
    parser.add_argument('file', help='CSV data file')
    parser.add_argument('--encoding', '-e', default='utf-8', help='CSV encoding')
    parser.add_argument('--output', '-o', help='Output .tex path (default: <file>_report.tex)')
    parser.add_argument('--compile', '-c', action='store_true', help='Also compile to PDF')
    parser.add_argument('--group-col', help='Column name for grouped comparison')
    parser.add_argument('--title', help='Report title')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    report = build_report(args.file, group_col=args.group_col, encoding=args.encoding)
    if args.title:
        report['title'] = args.title

    out_tex = args.output or os.path.splitext(args.file)[0] + '_report.tex'
    build_tex(report, out_tex)
    print(f"[OK] TeX generated: {out_tex}")

    if args.compile:
        import subprocess
        compile_py = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  'references', 'latex', 'scripts', 'compile.py')
        if os.path.exists(compile_py):
            subprocess.run(['uv', 'run', 'python', compile_py, out_tex], check=False)
        else:
            print("[WARN] compile.py not found, skipping PDF compilation")


if __name__ == '__main__':
    main()

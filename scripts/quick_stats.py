#!/usr/bin/env python3
"""快速数据概览 — 纯 Python 标准库，无需安装任何第三方包。

输出: 行数 / 列数 / 数据类型推断 / 缺失值 / 描述性统计 (mean, std, min, Q1, median, Q3, max, skew)

用法:
  python quick_stats.py data.csv
  python quick_stats.py data.csv --top 20     # 只输出前 20 行
  python quick_stats.py data.csv --encoding gbk

也可作为模块在分析脚本中调用:
  from quick_stats import scan_csv
  report = scan_csv('data.csv')
  print(report)
"""

import csv
import math
import sys
import os
from collections import Counter


def infer_type(values: list[str]) -> str:
    """推断列的数据类型。"""
    numeric_count = 0
    total = 0
    for v in values:
        if v.strip() == '':
            continue
        total += 1
        try:
            float(v)
            numeric_count += 1
        except ValueError:
            pass
    if total == 0:
        return 'empty'
    if numeric_count / total > 0.85:
        return 'numeric'
    if all(v.strip() in ('', '0', '1', 'True', 'False', 'true', 'false', 'yes', 'no') for v in values):
        return 'boolean'
    unique_ratio = len(set(v.strip() for v in values if v.strip())) / max(total, 1)
    if unique_ratio < 0.3 and total > 10:
        return 'categorical'
    return 'text'


def compute_stats(nums: list[float]) -> dict:
    """计算数值列的描述性统计。"""
    n = len(nums)
    if n == 0:
        return {'count': 0}
    sorted_nums = sorted(nums)
    mean = sum(nums) / n
    variance = sum((x - mean) ** 2 for x in nums) / (n - 1) if n > 1 else 0
    std = math.sqrt(variance)
    skew = sum(((x - mean) / std) ** 3 for x in nums) / n if std > 0 else 0

    def percentile(data, pct):
        k = (len(data) - 1) * pct
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        return data[f] * (c - k) + data[c] * (k - f)

    return {
        'count': n,
        'mean': round(mean, 4),
        'std': round(std, 4),
        'min': round(sorted_nums[0], 4),
        'q1': round(percentile(sorted_nums, 0.25), 4),
        'median': round(percentile(sorted_nums, 0.50), 4),
        'q3': round(percentile(sorted_nums, 0.75), 4),
        'max': round(sorted_nums[-1], 4),
        'skew': round(skew, 4),
    }


def scan_csv(filepath: str, encoding: str = 'utf-8') -> dict:
    """扫描 CSV 文件，返回结构化报告。"""
    # 自动检测编码
    if encoding == 'auto':
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    f.read(1024)
                encoding = enc
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

    rows = []
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)

    n_cols = len(header)
    n_rows = len(rows)

    # 转置列
    columns = {header[i]: [row[i] if i < len(row) else '' for row in rows] for i in range(n_cols)}

    # 类型推断
    col_types = {col: infer_type(vals) for col, vals in columns.items()}

    # 缺失值
    missing = {col: sum(1 for v in vals if v.strip() == '') for col, vals in columns.items()}

    # 数值列统计
    num_stats = {}
    for col, vals in columns.items():
        if col_types[col] == 'numeric':
            nums = []
            for v in vals:
                v = v.strip()
                if v != '':
                    try:
                        nums.append(float(v))
                    except ValueError:
                        pass
            num_stats[col] = compute_stats(nums)

    return {
        'file': filepath,
        'encoding': encoding,
        'n_rows': n_rows,
        'n_cols': n_cols,
        'header': header,
        'col_types': col_types,
        'missing': missing,
        'missing_pct': {col: round(m / max(n_rows, 1) * 100, 2) for col, m in missing.items()},
        'num_stats': num_stats,
    }


def report_markdown(report: dict) -> str:
    """将扫描结果格式化为 Markdown 报告。"""
    lines = []
    lines.append(f"## 数据快速概览: {os.path.basename(report['file'])}")
    lines.append(f"")
    lines.append(f"- 维度: {report['n_rows']} 行 × {report['n_cols']} 列")
    lines.append(f"- 编码: {report['encoding']}")
    lines.append(f"")

    # 列概要
    lines.append(f"### 列类型")
    type_counts = Counter(report['col_types'].values())
    lines.append(f"| 类型 | 数量 |")
    lines.append(f"|------|------|")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {c} |")
    lines.append(f"")

    # 缺失值
    if any(v > 0 for v in report['missing'].values()):
        lines.append(f"### 缺失值")
        lines.append(f"| 变量 | 缺失数 | 缺失比例 |")
        lines.append(f"|------|--------|----------|")
        for col in report['header']:
            if report['missing'][col] > 0:
                lines.append(f"| {col} | {report['missing'][col]} | {report['missing_pct'][col]}% |")
        lines.append(f"")

    # 数值统计
    if report['num_stats']:
        lines.append(f"### 描述性统计")
        for col, stats in report['num_stats'].items():
            if stats['count'] == 0:
                continue
            lines.append(f"**{col}** (N={stats['count']})")
            lines.append(f"| 指标 | 值 |")
            lines.append(f"|------|----|")
            lines.append(f"| Mean ± SD | {stats['mean']} ± {stats['std']} |")
            lines.append(f"| Min / Q1 / Med / Q3 / Max | {stats['min']} / {stats['q1']} / {stats['median']} / {stats['q3']} / {stats['max']} |")
            lines.append(f"| Skew | {stats['skew']} |")
            lines.append(f"")

    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fast CSV overview using stdlib only')
    parser.add_argument('file', help='CSV file path')
    parser.add_argument('--encoding', '-e', default='auto', help='File encoding (default: auto-detect)')
    parser.add_argument('--top', type=int, default=0, help='Show first N rows')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    report = scan_csv(args.file, args.encoding)

    if args.json:
        import json
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        print(report_markdown(report))

    if args.top > 0:
        print(f"\n### 前 {args.top} 行预览")
        with open(args.file, 'r', encoding=report['encoding']) as f:
            for i, line in enumerate(f):
                if i == 0:
                    print(line.rstrip())
                elif i <= args.top:
                    print(line.rstrip())
                else:
                    break


if __name__ == '__main__':
    main()

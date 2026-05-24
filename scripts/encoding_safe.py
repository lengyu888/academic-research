#!/usr/bin/env python3
"""Windows GBK 安全包装器 — 确保分析脚本输出不被终端编码截断。

问题：Windows 中文终端默认 GBK 编码，Python 输出含非 GBK 字符时会报
  UnicodeEncodeError: 'gbk' codec can't encode character ...

解决方案:
  - 作为模块导入时，自动设置 sys.stdout 为 UTF-8 兼容包装
  - 作为命令运行时，包装目标脚本

用法 1 — 包装目标脚本:
  python encoding_safe.py -- data_analysis.py --arg1 --arg2

用法 2 — 在分析脚本顶部嵌入:
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""

import sys
import io
import subprocess
import os


def safe_stdout():
    """将 stdout/stderr 包装为 UTF-8，失败字符用 ? 替换。"""
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding='utf-8',
            errors='replace',
            line_buffering=True,
        )
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer,
            encoding='utf-8',
            errors='replace',
            line_buffering=True,
        )


def is_windows_gbk() -> bool:
    """检测是否在 Windows GBK 环境。"""
    return sys.platform == 'win32' and sys.getdefaultencoding().lower() in ('gbk', 'gb2312', 'gb18030', 'cp936')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run script with UTF-8 safe stdout')
    parser.add_argument('script', help='Script to run')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the script')
    args = parser.parse_args()

    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8:replace'

    cmd = [sys.executable, args.script] + args.args
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    sys.exit(result.returncode)


if __name__ == '__main__':
    main()

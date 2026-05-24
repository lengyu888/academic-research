#!/usr/bin/env python3
"""依赖预检与自动安装 — 只装缺失的，不重复安装。

用法:
  python dep_check.py pandas numpy scipy matplotlib seaborn
  python dep_check.py pandas scipy  # 只装这两个

在分析脚本中嵌入:
  import subprocess, sys, importlib
  needed = ['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn']
  for pkg in needed:
      try: importlib.import_module(pkg)
      except ImportError:
          subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', pkg])
"""

import importlib
import subprocess
import sys
import time


def check_package(pkg: str) -> bool:
    """检查单个包是否已安装。"""
    try:
        importlib.import_module(pkg.replace('-', '_'))
        return True
    except ImportError:
        return False


def install_package(pkg: str, quiet: bool = True) -> bool:
    """安装单个包，返回是否成功。"""
    try:
        args = [sys.executable, '-m', 'pip', 'install']
        if quiet:
            args.append('-q')
        args.append(pkg)
        subprocess.check_call(args, timeout=300)
        return True
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to install {pkg}", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout installing {pkg}", file=sys.stderr)
        return False


def ensure(packages: list[str], quiet: bool = True) -> tuple[list[str], list[str]]:
    """确保所有包已安装。返回 (已安装列表, 失败列表)。"""
    installed = []
    failed = []
    missing = [p for p in packages if not check_package(p)]

    if not missing:
        return installed, failed

    print(f"[dep_check] Installing {len(missing)} missing package(s): {', '.join(missing)}")

    for pkg in missing:
        if install_package(pkg, quiet):
            installed.append(pkg)
        else:
            failed.append(pkg)

    return installed, failed


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Check and install Python dependencies')
    parser.add_argument('packages', nargs='+', help='Package names to check/install')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show pip output')
    parser.add_argument('--timeout', type=int, default=300, help='Per-package time limit (seconds)')
    args = parser.parse_args()

    start = time.time()
    installed, failed = ensure(args.packages, quiet=not args.verbose)

    for pkg in installed:
        print(f"[OK] {pkg} installed")
    for pkg in failed:
        print(f"[FAIL] {pkg} failed")

    already = [p for p in args.packages if p not in installed and p not in failed]
    if already:
        print(f"[SKIP] {len(already)} package(s) already present")

    elapsed = time.time() - start
    print(f"[dep_check] Done in {elapsed:.1f}s — {len(installed)} installed, {len(failed)} failed, {len(already)} skipped")

    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()

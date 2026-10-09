#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MANIFEST.csv 生成器：逐件登记 path/bytes/sha256。

用法（在数据仓根或任意子集上）：
    python scripts/update_manifest.py                    # 默认 outputs samples docs scripts
    python scripts/update_manifest.py --dirs outputs     # 只扫指定目录
    python scripts/update_manifest.py --out outputs/MANIFEST.csv

纪律：只读扫描，不改被登记件；.git 与 MANIFEST*.csv 自身排除。
"""
import argparse
import hashlib
import os


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    repo = argparse.ArgumentParser().__parser__ if False else None  # noqa: F841 (keep stdlib-only)
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=os.getcwd(), help="仓库根（默认当前目录）")
    ap.add_argument("--dirs", default="outputs,samples,docs,scripts", help="逗号分隔的扫描目录")
    ap.add_argument("--out", default="MANIFEST.csv", help="输出 CSV（相对 root）")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_path = os.path.join(root, args.out)
    rows = []
    for d in [x.strip() for x in args.dirs.split(",") if x.strip()]:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            print(f"[WARN] 跳过不存在的目录: {d}")
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x != ".git"]
            for name in sorted(filenames):
                if name.startswith("MANIFEST") and name.endswith(".csv"):
                    continue
                p = os.path.join(dirpath, name)
                rel = os.path.relpath(p, root)
                size = os.path.getsize(p)
                if size > 25 * 1024 * 1024:
                    print(f"[WARN] 超过 25MB 建议阈值（仍登记）: {rel} {size}")
                rows.append((rel, size, sha256_of(p)))

    rows.sort()
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("path,bytes,sha256\n")
        for rel, size, digest in rows:
            f.write(f"{rel},{size},{digest}\n")
    print(f"[OK] {len(rows)} 件 → {os.path.relpath(out_path, root)}")


if __name__ == "__main__":
    main()

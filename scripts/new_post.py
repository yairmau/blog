#!/usr/bin/env python3
"""Create a Quarto post without third-party packages."""

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]


def slugify(title):
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", help="Post title (prompted if omitted)")
    parser.add_argument("--categories", help="Comma-separated categories (prompted if omitted)")
    parser.add_argument("--slug", help="Optional URL slug using letters, numbers, and hyphens")
    parser.add_argument("--date", type=date.fromisoformat, help="Publication date, YYYY-MM-DD")
    parser.add_argument("--open", action="store_true", help="Open the post in VS Code")
    args = parser.parse_args()
    title = (args.title if args.title is not None else input("Title: ")).strip()
    if not title or any(ord(c) < 32 for c in title):
        parser.error("Provide a nonempty, single-line title.")
    slug = args.slug if args.slug is not None else slugify(title)
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        parser.error("Provide --slug using lowercase ASCII letters, numbers, and hyphens.")
    raw_categories = args.categories
    if raw_categories is None:
        raw_categories = input("Categories (comma-separated, optional): ")
    categories = list(dict.fromkeys(c.strip() for c in raw_categories.split(",") if c.strip()))
    post_date = args.date or datetime.now(ZoneInfo("Asia/Jerusalem")).date()
    directory = ROOT / "posts" / f"{post_date.isoformat()}-{slug}"
    try:
        directory.mkdir()  # Refuse collisions; never overwrite an existing post.
    except FileExistsError:
        parser.error(f"Post folder already exists: {directory}")
    post = directory / "index.qmd"
    # JSON strings and arrays are valid YAML, including quotes and punctuation.
    post.write_text(
        f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\n"
        f"date: {post_date.isoformat()}\n"
        f"categories: {json.dumps(categories, ensure_ascii=False)}\n"
        "---\n\n",
        encoding="utf-8",
    )
    print(f"Created {post}")
    if args.open:
        code = shutil.which("code")
        mac_code = Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")
        if code is None and mac_code.is_file():
            code = str(mac_code)
        if code:
            try:
                subprocess.run([code, "--reuse-window", str(post)], check=True)
            except (OSError, subprocess.CalledProcessError) as error:
                print(f"Post saved; open it manually in VS Code ({error}).")
        else:
            print("Post saved; open it in VS Code, or install the 'code' shell command.")


if __name__ == "__main__":
    main()

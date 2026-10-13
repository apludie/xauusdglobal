#!/usr/bin/env python3
"""Create an offline copy of the built site that opens by double-clicking index.html.

    python3 _build/make_preview.py  ->  ../xauusdglobal-offline-preview/

Root-relative links (/blog/) are rewritten to relative file links (../blog/index.html).
Use this copy ONLY for previewing on your computer. Deploy the main folder, not this one.
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(ROOT), "xauusdglobal-offline-preview")


def relativize(html, depth):
    prefix = "../" * depth

    def fix(m):
        attr, path = m.group(1), m.group(2)
        frag = ""
        if "#" in path:
            path, frag = path.split("#", 1)
            frag = "#" + frag
        path = path.lstrip("/")
        if path == "" or path.endswith("/"):
            path += "index.html"
        return f'{attr}="{prefix}{path}{frag}"'

    html = re.sub(r'(href|src)="(/(?!/)[^"]*)"', fix, html)
    html = html.replace('data-news-feed="/', f'data-news-feed="{prefix}')
    return html


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(ROOT, OUT, ignore=shutil.ignore_patterns("_build", ".git", "__pycache__", "README.md", "CNAME", "_config.yml"))
    for dirpath, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                fp = os.path.join(dirpath, f)
                depth = os.path.relpath(dirpath, OUT).count(os.sep) + (0 if dirpath == OUT else 1)
                html = open(fp, encoding="utf-8").read()
                html = relativize(html, depth)
                html = html.replace("<body ", '<body data-offline-preview="1" ', 1)
                open(fp, "w", encoding="utf-8").write(html)
    open(os.path.join(OUT, "READ-ME-FIRST.txt"), "w").write(
        "OFFLINE PREVIEW ONLY\n\nDouble-click index.html to browse the site on your computer.\n"
        "Do NOT upload this folder to GitHub. Upload the main 'xauusdglobal' folder instead.\n"
        "The live TradingView chart may not load from a local file; it will work on the real website.\n")
    print("Offline preview written to", OUT)


if __name__ == "__main__":
    main()

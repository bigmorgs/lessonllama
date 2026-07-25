#!/usr/bin/env python3
"""
Receives a Lesson Llama blog post from the Hermes agent via stdin,
creates a Markdown file in src/content/blog/, and opens a GitHub PR.

Input format (same as the old Hashnode draft flow):

SUGGESTED TITLE: [title]
TARGET KEYWORD: [keyword]
META DESCRIPTION: [under 160 chars]

[full blog post in Markdown]

Environment expectations:
- Runs from inside the site repo clone.
- git user.name and user.email are configured.
- `gh` CLI is authenticated and can open PRs.
- The remote `origin` has write access.
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(os.environ.get("LESSONLLAMA_REPO", Path(__file__).resolve().parent.parent))
BLOG_DIR = REPO_ROOT / "src" / "content" / "blog"


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    s = re.sub(r"-+", "-", s)
    return s or "untitled"


def parse_input(text: str) -> dict:
    text = text.strip()

    title_match = re.search(r"^SUGGESTED TITLE:\s*(.+)$", text, re.MULTILINE)
    tags_match = re.search(r"^TAGS:\s*(.+)$", text, re.MULTILINE)
    keyword_match = re.search(r"^TARGET KEYWORD:\s*(.+)$", text, re.MULTILINE)
    meta_match = re.search(r"^META DESCRIPTION:\s*(.+)$", text, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else "Untitled"
    description = meta_match.group(1).strip() if meta_match else ""

    tags = []
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(",") if t.strip()]
    elif keyword_match:
        tags = [keyword_match.group(1).strip()]

    # Body starts after the meta description line, after a blank line.
    if meta_match:
        body_start = meta_match.end()
        body = text[body_start:].strip()
    else:
        body = text

    # Strip a possible trailing "Deliver..." or script instruction the agent
    # might have added by mistake.
    body = re.sub(r"\n?(After generating the post|Deliver the draft URL|Create a PR).*", "", body, flags=re.IGNORECASE).strip()

    return {
        "title": title,
        "tags": tags,
        "description": description,
        "body": body,
    }


def run(cmd: list[str], check: bool = True) -> str:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        print("No input received.", file=sys.stderr)
        sys.exit(1)

    post = parse_input(raw)
    slug = slugify(post["title"])
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    tags = ", ".join(repr(t) for t in post["tags"]) if post["tags"] else ""

    frontmatter = f"""---
title: {post['title']!r}
description: {post['description']!r}
pubDate: {pub_date}
tags: [{tags}]
---

"""

    file_path = BLOG_DIR / f"{slug}.md"
    if file_path.exists():
        print(f"ERROR: {file_path} already exists.", file=sys.stderr)
        sys.exit(1)

    file_path.write_text(frontmatter + post["body"] + "\n", encoding="utf-8")

    run(["git", "checkout", "main"])
    run(["git", "pull", "--rebase", "origin", "main"])

    branch = f"post/{slug}"
    run(["git", "checkout", "-b", branch])
    run(["git", "add", str(file_path.relative_to(REPO_ROOT))])
    run(["git", "commit", "-m", f"blog: add {slug}"])
    run(["git", "push", "-u", "origin", branch])

    pr_url = run(
        [
            "gh", "pr", "create",
            "--title", f"Blog post: {post['title']}",
            "--body", f"New blog post: {post['description']}\n\nSlug: `{slug}`",
        ]
    )

    print(pr_url)


if __name__ == "__main__":
    main()

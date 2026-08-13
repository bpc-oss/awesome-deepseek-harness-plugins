#!/usr/bin/env python3
"""Fetch DeepSeek Harness (DSH) plugins from GitHub and emit a markdown table.

Uses the public GitHub Search API. Any token via GITHUB_TOKEN raises the rate
limit; without one the script still works (lower limit). The main repo
deepseek-ai/deepseek-harness is excluded.

    python scripts/fetch_plugins.py > PLUGINS.md
"""
import json
import os
import sys
import urllib.parse
import urllib.request
import datetime

API = "https://api.github.com/search/repositories"
QUERIES = [
    "topic:dsh-plugin",
    "deepseek-harness plugin in:name,description,readme",
    "dsh-plugin in:name,description,readme",
]
HEADERS = {"Accept": "application/vnd.github+json"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"Bearer {token}"


def search(q: str):
    params = urllib.parse.urlencode(
        {"q": q, "per_page": 100, "sort": "stars", "order": "desc"}
    )
    req = urllib.request.Request(f"{API}?{params}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("items", [])


def main() -> None:
    seen = {}
    for q in QUERIES:
        try:
            for it in search(q):
                name = it["full_name"]
                if name == "deepseek-ai/deepseek-harness":
                    continue
                if name not in seen or it["stargazers_count"] > seen[name]["stargazers_count"]:
                    seen[name] = it
        except Exception as e:  # noqa: BLE001
            print(f"# warning: query failed ({q}): {e}", file=sys.stderr)

    items = sorted(seen.values(), key=lambda x: x["stargazers_count"], reverse=True)
    today = datetime.date.today().isoformat()
    lines = [
        "# DSH Plugins Snapshot",
        "",
        f"> Auto-generated from the GitHub Search API on {today}. This is a raw, "
        "unmoderated index sorted by stars. For the curated, categorized view see "
        "[README.md](README.md).",
        "",
        "To refresh: `python scripts/fetch_plugins.py > PLUGINS.md`",
        "",
        "| Stars | Repository | Description |",
        "|------:|------------|-------------|",
    ]
    for it in items:
        desc = (it.get("description") or "").replace("|", "\\|").replace("\n", " ")
        desc = desc[:200]
        lines.append(
            f"| {it['stargazers_count']} | "
            f"[{it['full_name']}]({it['html_url']}) | {desc} |"
        )
    print("\n".join(lines))


if __name__ == "__main__":
    main()

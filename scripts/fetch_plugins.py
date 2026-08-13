#!/usr/bin/env python3
"""Fetch DeepSeek Harness (DSH) plugins from GitHub and emit a markdown table.

Uses the public GitHub Search API. Any token via GITHUB_TOKEN raises the rate
limit; without one the script still works (lower limit).

Strategy:
  * Query ONLY `topic:dsh-plugin` — the precise topic the community agreed on.
    Broad keyword queries (e.g. "plugin", "deepseek-harness") pull in unrelated
    repos (awesome-sysadmin, awesome-ssh, Self-Hosting-Guide, …) that merely
    mention those words, which pollutes the list.
  * Page through all results (GitHub caps search at 1000 hits / 10 pages).
  * Keep only entries whose name or description references DeepSeek / Harness /
    DSH / Cordis, so mistagged non-DSH repos are dropped.

    python scripts/fetch_plugins.py > PLUGINS.md
"""
import json
import os
import sys
import urllib.parse
import urllib.request
import datetime

API = "https://api.github.com/search/repositories"
QUERY = "topic:dsh-plugin"
SIGNAL = ("deepseek", "harness", "dsh", "cordis", "deepseek-ai")
HEADERS = {"Accept": "application/vnd.github+json"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"Bearer {token}"


def search(q: str, page: int):
    params = urllib.parse.urlencode(
        {"q": q, "per_page": 100, "page": page, "sort": "stars", "order": "desc"}
    )
    req = urllib.request.Request(f"{API}?{params}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("items", [])


def is_relevant(it: dict) -> bool:
    text = (it["full_name"] + " " + (it.get("description") or "")).lower()
    return any(k in text for k in SIGNAL)


def main() -> None:
    seen = {}
    page = 1
    while page <= 10:  # GitHub search hard-caps at 1000 results
        try:
            items = search(QUERY, page)
        except Exception as e:  # noqa: BLE001
            print(f"# warning: page {page} failed: {e}", file=sys.stderr)
            break
        if not items:
            break
        for it in items:
            name = it["full_name"]
            if name == "deepseek-ai/deepseek-harness":
                continue
            if not is_relevant(it):
                continue
            if name not in seen or it["stargazers_count"] > seen[name]["stargazers_count"]:
                seen[name] = it
        if len(items) < 100:
            break
        page += 1

    items = sorted(seen.values(), key=lambda x: x["stargazers_count"], reverse=True)
    today = datetime.date.today().isoformat()
    lines = [
        "# DSH Plugins Snapshot",
        "",
        f"> Auto-generated from the GitHub Search API on {today}. This index is "
        "built from the `dsh-plugin` topic and filtered to DeepSeek-Harness-"
        "related repos; it is sorted by stars and NOT hand-curated. For the "
        "curated, categorized view see [README.md](README.md).",
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

#!/usr/bin/env python3
"""Rule-based reviewer for plugin-submission PRs (Channel B of CONTRIBUTING).

Triggered by .github/workflows/review-pr.yml. It NEVER checks out or executes
untrusted PR code — it only reads the PR's README.md at the head SHA via the
GitHub API and validates each *newly added* repo reference against a fixed rule
set. Output:
  * a Markdown report printed to stdout (posted as a PR comment by the workflow)
  * a machine-readable JSON summary written to review_result.json

Exit code is 0 regardless of pass/fail (the workflow decides what to do); the
verdict lives in review_result.json["pass"].

Rules
-----
R1  Only README.md may be modified by contributors.
R2  Every newly added repo must exist and be public.
R3  Every added repo must be clearly DSH-related: it must carry the
    `dsh-plugin` topic OR its name/description must match a relevance signal
    (English + Chinese).
R4  No added repo may already be listed in the base README (no duplicates).
R5  (soft) `dsh plugin add <pkg>` install commands must be well formed.

    python scripts/review_pr.py
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

API = "https://api.github.com"
REPO = os.environ["GITHUB_REPOSITORY"]          # owner/name
PR_NUMBER = os.environ["PR_NUMBER"]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

# Same relevance signals as fetch_plugins.py.
SIGNAL = (
    "deepseek", "harness", "dsh", "cordis", "deepseek-ai", "cordiverse",
    "外挂", "插件", "深度求索",
)
REPO_RE = re.compile(
    r"(?:github\.com/|github:)([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"
)
ALLOWED_FILES = {"README.md"}


def api(path: str) -> tuple[int, dict | list | None]:
    req = urllib.request.Request(f"{API}{path}", headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except Exception:
            return e.code, None
    except Exception as e:  # noqa: BLE001
        print(f"# warning: api {path} failed: {e}", file=sys.stderr)
        return 0, None


def get_file_content(ref: str) -> str | None:
    status, data = api(f"/repos/{REPO}/contents/README.md?ref={ref}")
    if status != 200 or not isinstance(data, dict):
        return None
    import base64
    return base64.b64decode(data.get("content", "")).decode("utf-8", "replace")


def repos_in(text: str) -> set[tuple[str, str]]:
    out = set()
    for m in REPO_RE.finditer(text or ""):
        out.add((m.group(1), m.group(2).rstrip(").#& ")))
    # drop the framework itself and obvious non-repo matches
    out.discard(("deepseek-ai", "deepseek-harness"))
    return out


def is_dsh_related(name: str, data: dict) -> bool:
    text = (name + " " + (data.get("description") or "")).lower()
    return any(k.lower() in text for k in SIGNAL)


def main() -> None:
    report = []
    checks = []

    # --- PR metadata ---
    status, pr = api(f"/repos/{REPO}/pulls/{PR_NUMBER}")
    if status != 200 or not isinstance(pr, dict):
        report.append("❌ Could not load PR metadata.")
        json.dump({"pass": False, "reason": "pr_load_failed",
                   "only_readme": False, "repos": [], "labels": ["needs-review"]},
                  open("review_result.json", "w"))
        print("\n".join(report))
        return

    base_sha = pr["base"]["sha"]
    head_sha = pr["head"]["sha"]
    author = pr["user"]["login"]

    # --- R1: only README.md changed ---
    status, files = api(f"/repos/{REPO}/pulls/{PR_NUMBER}/files?per_page=100")
    changed = [f["filename"] for f in (files or [])]
    only_readme = set(changed) <= ALLOWED_FILES and "README.md" in changed
    if only_readme:
        checks.append("✅ R1 Only README.md was modified.")
    else:
        extras = [f for f in changed if f not in ALLOWED_FILES]
        checks.append(f"❌ R1 Non-README files changed: {', '.join(extras)}. "
                      "Contributors may only edit README.md.")

    # --- load README versions ---
    base_md = get_file_content(base_sha) or ""
    head_md = get_file_content(head_sha) or ""
    if not head_md:
        report.append("❌ Could not read the PR's README.md.")
        json.dump({"pass": False, "reason": "readme_load_failed",
                   "only_readme": only_readme, "repos": [],
                   "labels": ["needs-review"]},
                  open("review_result.json", "w"))
        print("\n".join(report))
        return

    added = repos_in(head_md) - repos_in(base_md)
    removed = repos_in(base_md) - repos_in(head_md)

    # --- R2/R3/R4 per added repo ---
    repo_results = []
    for owner, name in sorted(added):
        full = f"{owner}/{name}"
        st, data = api(f"/repos/{owner}/{name}")
        if st != 200 or not isinstance(data, dict):
            repo_results.append({"repo": full, "ok": False,
                                 "why": "repository not found or private"})
            continue
        has_topic = "dsh-plugin" in (data.get("topics") or [])
        related = is_dsh_related(full, data)
        if not (has_topic or related):
            repo_results.append({
                "repo": full, "ok": False,
                "why": "not clearly a DSH plugin — add the `dsh-plugin` topic "
                       "or mention DeepSeek Harness / DSH in the description"})
            continue
        if (owner, name) in repos_in(base_md):
            repo_results.append({"repo": full, "ok": False,
                                 "why": "already listed (duplicate)"})
            continue
        repo_results.append({"repo": full, "ok": True, "why": "ok"})

    # --- R5 (soft): install command format ---
    # Capture only real package tokens (no backticks / angle brackets), so the
    # README's own `<npm-package>` placeholders and inline-code `` `dsh plugin
    # add` `` occurrences are ignored. A genuinely malformed token would still
    # be flagged here.
    bad_cmds = []
    for m in re.finditer(r"dsh\s+plugin\s+add\s+([^\s`<>]+)", head_md):
        pkg = m.group(1)
        if not re.match(r"^[A-Za-z0-9_@/.\-]+$", pkg):
            bad_cmds.append(pkg)

    # --- summary ---
    r2r4_ok = all(r["ok"] for r in repo_results) if repo_results else True
    checks.append(
        f"{'✅' if r2r4_ok else '❌'} R2–R4 "
        f"{len(repo_results)} new plugin repo(s) validated."
    )
    for r in repo_results:
        mark = "✅" if r["ok"] else "❌"
        checks.append(f"   {mark} `{r['repo']}` — {r['why']}")
    if not repo_results:
        checks.append("   (no new plugin repo detected in this PR)")
    if bad_cmds:
        checks.append("⚠️ R5 Malformed install command(s): "
                      + ", ".join(f"`{c}`" for c in bad_cmds)
                      + " — expected `dsh plugin add <pkg>`.")
    else:
        checks.append("✅ R5 Install commands well formed (or none).")

    if removed:
        checks.append(f"ℹ️ Removed {len(removed)} repo reference(s): "
                      + ", ".join(f"{o}/{n}" for o, n in sorted(removed)))

    passed = only_readme and r2r4_ok
    labels = ["auto-approved"] if passed else ["needs-review"]
    if not only_readme:
        labels.append("changes-requested")

    verdict = "✅ **AUTO-APPROVED** — all rules passed; will be auto-merged." \
        if passed else "❌ **CHANGES REQUESTED** — fix the items above and push."

    report = [
        f"## Plugin submission review — PR #{PR_NUMBER} by @{author}",
        "",
        verdict,
        "",
        "### Rules",
        *checks,
        "",
        "> Reviewed automatically by `review-pr.yml` against the rules in "
        "CONTRIBUTING.md. A maintainer can still override.",
    ]

    json.dump({
        "pass": passed,
        "only_readme": only_readme,
        "repos": repo_results,
        "labels": labels,
        "bad_commands": bad_cmds,
    }, open("review_result.json", "w"), ensure_ascii=False, indent=2)

    print("\n".join(report))


if __name__ == "__main__":
    main()

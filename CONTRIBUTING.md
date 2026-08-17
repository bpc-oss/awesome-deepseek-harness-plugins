# Contributing to Awesome DeepSeek Harness Plugins

There are two ways to get a plugin into this list. **You only need one.**

## Channel A — Zero maintenance (recommended)

1. Go to your plugin's GitHub repository.
2. Add the topic **`dsh-plugin`** (Settings → Topics, or the repo's "About"
   sidebar).
3. That's it. [PLUGINS.md](PLUGINS.md) is regenerated **every day** by
   [update.yml](.github/workflows/update.yml) from the `dsh-plugin` topic via the
   GitHub Search API. Your repo shows up in the snapshot within ~24h — no PR
   required.

Caveats for Channel A:
- The snapshot only includes repos that **actually carry the `dsh-plugin`
  topic**. Tagging is the whole mechanism.
- A repo is dropped from the snapshot if it loses the topic, goes private, or is
  deleted.
- Relevance is filtered by signal keywords (English + Chinese): `deepseek`,
  `harness`, `dsh`, `cordis`, `deepseek-ai`, `cordiverse`, `外挂`, `插件`,
  `深度求索`. A repo whose name/description mentions none of these (and has no
  topic) won't be included. If your repo is DSH-related but gets missed, add the
  topic or a keyword to the description.

## Channel B — Curated README (auto-reviewed)

Want your plugin in the hand-categorized [README.md](README.md) (nicer
presentation, grouped by use case)? Open a pull request that adds it under the
right section, with a one-line description and a star-count snapshot.

The PR is **automatically reviewed by rules** — there is no human gate. The
[review-pr.yml](.github/workflows/review-pr.yml) workflow runs
[scripts/review_pr.py](scripts/review_pr.py), which:

- reads **only** the PR's `README.md` at the head commit via the GitHub API
  (it never checks out or executes PR code, so it is safe for fork PRs);
- compares the base and head README to find **newly added** repo references;
- validates each one.

### Review rules

| # | Rule | Failure message |
|---|------|-----------------|
| R1 | The PR must change **only `README.md`** | "Non-README files changed" |
| R2 | Every added repo must **exist and be public** | "repository not found or private" |
| R3 | Every added repo must be **clearly DSH-related**: it carries the `dsh-plugin` topic **OR** its name/description matches a signal keyword (`deepseek` / `harness` / `dsh` / `cordis` / `deepseek-ai` / `cordiverse` / `外挂` / `插件` / `深度求索`) | "not clearly a DSH plugin — add the `dsh-plugin` topic or mention DeepSeek Harness / DSH in the description" |
| R4 | No added repo may **already be listed** in the base README | "already listed (duplicate)" |
| R5 | (soft) `dsh plugin add <pkg>` install commands must be well formed | warning only, never blocks |

### Outcome

- **All rules pass** → the PR is labeled `auto-approved` and **automatically
  squash-merged**.
- **Any rule fails** → the PR is labeled `changes-requested` (and the non-README
  case also gets `changes-requested`) with a comment listing exactly what to
  fix. Push a fix and the review re-runs automatically.
- A **maintainer can always override** — the automation is a convenience, not a
  lock. Manual merge/close still works.

### Tips for a clean Channel-B PR

- Put the entry under the most specific existing section.
- Use the repo-hosted form `github:<owner>/<repo>` or the npm form
  `dsh plugin add <npm-package>` for the install line.
- Don't touch `PLUGINS.md` — it is generated; edits will be overwritten and will
  fail R1.

## Security note

`review-pr.yml` uses `pull_request_target` so it can comment, label, and merge
fork PRs. It is deliberately written to **never run code from the PR**: the
review script is always the trusted version from the base branch, and it only
inspects README text and public repo metadata through the API. Auto-merge is
gated strictly on the rules above (single-file change + valid public DSH repos).
If you want an extra safety net, enable branch protection requiring a
maintainer review before merges.

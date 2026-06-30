# AGENTS.md — mcp-bench: how we build this together

Two AI builders work in this repo, alongside the operator (Alex, pseudonym **StellarRequiem**):

- **Fade** (Claude) — corpus design, methodology, statistics, the core harness, tests.
- **Codex** (gpt-5.5) — scanner integration, CI/workflow, adversarial review of the corpus.

Read this before touching anything. It is the coordination contract — day-to-day status, handoffs,
and notes to each other go on the live board, not here.

> **LIVE BOARD → [`BOARD.md`](./BOARD.md)** — the single shared space for current work, handoffs, file
> locks, and notes to each other. This file (AGENTS.md) is the stable contract. Always re-read both
> before editing either; never overwrite the other agent's text, append instead.

## The product

**mcp-bench** — an independent, reproducible benchmark of whether MCP security scanners actually
catch *authorization-logic* vulnerabilities (broken object-level auth, confidential-secret exposure,
operation-filter bypass — the class behind real high-impact incidents), not just the easy/generic
classes. It measures detection + false-positive rate on a labeled corpus and reports the truth either
way — "scanners are good" is an equally valid, equally reportable result. See `README.md` and
`CORPUS_METHODOLOGY.md`.

## Hard invariants — NEVER break these (both agents)

1. **Untrusted code never touches the host.** Scanners (semgrep, bandit, dlint, Pysa, anything else)
   are third-party code we did not write. They run **only inside the disposable GitHub Actions
   ephemeral runner** (`.github/workflows/scan.yml`), never the primary host. Locally, a scanner is
   invoked only if `shutil.which()` finds it already installed — i.e. effectively never on a dev
   machine — so the local test suite stays host-safe by construction. New scanners must follow this
   exact pattern (an `*_available()` gate + a CI-only install step), not bypass it for convenience.
2. **The methodology in `CORPUS_METHODOLOGY.md` is pre-registered, not advisory.** No authz-logic
   case is rewritten after seeing how a scanner scores against it (control cases may be tuned to be
   *detectable* — that's their job; authz-logic cases never are). New authz-logic cases cite a CWE
   number and the abstract mechanism only — **never a real target name or finding ID** for anything
   not already publicly disclosed (a public CVE number is fine to cite directly; an internal/private
   finding is not, regardless of how confident the framing). If a methodology RULE needs to change
   (not just a new case), say so explicitly in the commit — that's a methodology change, not a corpus
   addition, and should be flagged as one.
3. **Gate every change.** `.venv/bin/python -m pytest tests/` must pass AND a live
   `.venv/bin/mcpbench run && .venv/bin/mcpbench score` must produce a sane, inspected result before
   a commit. No exceptions.
4. **Pseudonym identity, every commit.** `git -c user.name=StellarRequiem -c user.email=stellarrequiem@users.noreply.github.com`
   (already the repo's established convention — confirmed via `git log`). PII-gate every diff before
   committing — `git diff --cached | grep -ci` for the operator's real first/last name, personal email
   domain, and home-directory path, as a **separate step before the commit**, not chained with `&&`
   into one command. A non-zero count means STOP and inspect the matched line(s) before deciding —
   most hits are real leaks, but a line that's *documenting the gate itself* (like this one, which
   deliberately avoids spelling out the actual trigger strings so it doesn't perpetually false-positive
   on itself) is the one legitimate exception, and even that judgment call gets made by reading the
   match, never by assuming.
5. **Pushing is a separate, operator-gated step.** Unlike Realm (`~/realm-engine`, which never has a
   remote at all), **this repo IS public** (`github.com/StellarRequiem/mcp-bench`) and commits here
   eventually go live. Commit freely and often — that's just local git history. **Never run `git push`
   without the operator's explicit go-ahead for that specific push**, every time, no matter how
   confident the change is. Publishing to a public repo is the same category of action as sending a
   message on the operator's behalf — it needs a yes, not an inference from "they seemed happy with
   the last batch."
6. **No untrusted deps without sign-off.** Adding a new scanner/dependency to `pyproject.toml` or the
   CI workflow is fine to *try* and commit; flag it clearly on the board before it's something either
   agent assumes is now load-bearing.
7. One commit = one coherent change. Comments explain WHY, not WHAT.

## Layer split / file ownership (a starting proposal — refine on the board as real coordination happens)

**Fade owns — corpus / methodology / core harness:**
- `corpus/*`, `CORPUS_METHODOLOGY.md`
- `mcpbench/__init__.py` core logic (`load_cases`, `score`, `wilson_ci`, the scoring rule itself)
- `tests/*`

**Codex owns — scanner integration / CI:**
- Wiring a new scanner into `mcpbench/__init__.py` (an `*_available()` + `*_scan()` + a `parse_*`
  function, following the existing `semgrep`/`bandit` pattern exactly) and its `SCANNERS` dict entry.
- `.github/workflows/scan.yml` and `.github/workflows/ci.yml`.
- Adversarial review of Fade's corpus cases — a genuinely independent pair of eyes is worth more here
  than on most code, since one author designing all the "vulnerable" and "clean" cases risks blind
  spots a second reviewer catches (does the "clean" counterpart actually close the gap it claims to?).

**Shared, append-don't-overwrite:** `README.md`, `AGENTS.md`, `BOARD.md`.

This split is new (set up 2026-06-30) — unlike Realm's art/systems divide, mcp-bench doesn't have an
obvious orthogonal split, so treat the above as a proposal to confirm/adjust on the board once real
back-and-forth starts, not a fixed assignment.

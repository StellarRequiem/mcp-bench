# BOARD — mcp-bench shared workload board (Fade ⟷ Codex)

**THE single space** where both AI builders post what they're doing and update each other.
Operator-mandated 2026-06-30. The stable *contract* lives in [`AGENTS.md`](./AGENTS.md); **this is
the LIVE board** — current work, handoffs, locks, and notes to each other go here.

Builders: **Fade** (Claude) = corpus / methodology / statistics / core harness · **Codex** (gpt-5.5)
= scanner integration / CI / adversarial review.

## How to use this board (both agents, every work burst)

1. **Before editing any shared/contended file** (`BOARD.md`, `AGENTS.md`, `mcpbench/__init__.py`,
   `.github/workflows/*`): `git -C ~/mcp-bench status` + re-read the file. If the other agent has
   uncommitted work there, **do not overwrite** — append your own section, wait, or hand off. Never
   wholesale-replace the other's text.
2. **Claim it in "Now"** when you start a task; update/replace your own row when you finish.
3. **Commit stable states promptly** (small, one-coherent-change commits — `pytest` green + a live
   `mcpbench run`/`score` sanity check, every time) so the other agent rebases on committed work, not
   half-edits.
4. **Append one line to the Updates log** on each finished slice, handoff, or blocker.
5. **Never `git push`** without the operator's explicit go-ahead for that specific push (AGENTS.md
   §5) — commits are free; publishing to the public repo is not.

## Now (live — who's doing what)

| Agent | Lane | Current task | Files | Status |
|-------|------|--------------|-------|--------|
| Fade | corpus/methodology/stats | **STANDING BY (operator-directed 2026-06-30) — waiting for Codex's pass before anything pushes.** Phase-2 corpus hardening done for now: pre-registered methodology, then 8 new authz-logic cases + 3 clean counterparts, built and verified in 4 small commits (one per coherent batch, never rewriting a case after seeing how the reference scanner scored it). Corpus is 8→19 cases. **Not touching mcp-bench further** (no more corpus work, no push) until Codex has reviewed/worked and the operator says go — re-check this board before assuming the lane is still open. | `corpus/*`, `CORPUS_METHODOLOGY.md`, `mcpbench/__init__.py` (Wilson CI), `tests/test_pipeline.py` | 5 commits this session, all LOCAL ONLY — not pushed to origin (confirmed via `git log origin/main..HEAD`): `cf66939` (Wilson 95% CI), `ad069a6` (cases 1-3 + 2 clean), `5240d39` (cases 4-6 + 1 clean — an honest correction: `guard-divergence-across-paths` was incidentally caught by the existing naive regex, reported not hidden), `9e13d62` (cases 7-8), `e9baa63` (this board + AGENTS.md). 19 cases total (11 authz-logic + 2 control + 6 clean), reference scanner 4/11 detected, 0/6 false positives. Operator: "lets give codex a pass and then we will push." |
| Codex | scanner integration / CI (open) | **Open lane — claim it here when picked up.** Proposed next: (1) re-run semgrep against the fuller default registry packs (`p/owasp-top-ten`, `p/security-audit`, in addition to the already-used `p/python`/`p/secrets`) before any new scanner is added — an inconvenient catch from an untried default pack gets reported, not omitted (CORPUS_METHODOLOGY.md's own anti-p-hacking commitment). (2) `dlint` integration — cheap, Python-native, a real shot at non-zero control-case detection on a *differently-built* tool (linter-based, not taint-based like semgrep). (3) A Pysa/Pyre attempt — budget for an honest CodeQL-style revert if it can't run cleanly in the CI sandbox without hand-written taint configs; that's a legitimate, reportable outcome, not a failure. Each new scanner: an `*_available()` gate (host-safe by construction, AGENTS.md §1) + a `parse_*` function + a `SCANNERS` dict entry, following the existing `semgrep_scan`/`bandit_scan` pattern exactly. | `mcpbench/__init__.py` (new scanner wiring), `.github/workflows/scan.yml`, `pyproject.toml` | Not started. |

## File ownership / locks (quick reference — see AGENTS.md §"Layer split" for the full rationale)

- `corpus/*`, `CORPUS_METHODOLOGY.md`, `mcpbench/__init__.py` core scoring logic, `tests/*` → **Fade**.
- New scanner wiring in `mcpbench/__init__.py`, `.github/workflows/*` → **Codex**.
- `README.md`, `AGENTS.md`, `BOARD.md` → either may **append**; re-read first; don't replace the
  other's section.

## Handoff queue

- (Fade → Codex) Scanner-integration phase is open and unclaimed — see Codex's "Now" row above for
  the proposed sequencing. Pick it up, or propose a different lane on this board if scanner
  integration doesn't fit; the split in AGENTS.md is a starting proposal, not fixed.
- (Codex → Fade) Any new authz-logic case Codex wants to propose: design it from a real CWE-grounded
  pattern per CORPUS_METHODOLOGY.md's abstraction + disclosure-floor rules, and flag it here for
  Fade to review before merging into the corpus (mirrors the "adversarial review" lane — review runs
  both directions, not just Codex reviewing Fade).

## Updates log (append, don't rewrite — newest at the bottom)

- 2026-06-30 — **Fade**: board + contract set up (operator-directed: "create a surface for codex to
  collaborate... a document where you update each other's turns and direction"), modeled directly on
  `~/realm-engine/BOARD.md` + `AGENTS.md` (the proven Fade⟷Codex pattern), adapted for mcp-bench's
  real differences from Realm: this repo is **public** and gets pushed (with explicit per-push
  operator sign-off, AGENTS.md §5) rather than never-pushed; the Fade/Codex split is corpus-vs-
  scanner-integration rather than systems-vs-art, since there's no obvious art axis here. Seeded with
  the current, accurate state: 19-case corpus, 4 local-only unpushed commits, scanner-integration
  phase open and proposed (not assigned) to Codex. Nothing pushed to origin; nothing claimed on
  Codex's behalf beyond a proposal Codex/the operator can adjust.

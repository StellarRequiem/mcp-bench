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
| Fade | corpus/methodology/stats | **Headline verified + hardened, now PUSHED; conversation↔disk desync RECONCILED (2026-06-30) — see Updates-log tail. `5068911` (headline) + `c28aebc` (dlint) both public; nothing left unpushed.** Pulled the real CI scan artifact (run `28482069463`): semgrep+bandit now **0/11** authz-logic with fuller packs, vs the old 0/3. Ran a 4-way adversarial verification workflow before trusting that as a headline — clean, two honest caveats now disclosed (10 distinct classes not 11 independent trials; one missing clean counterpart). Added LICENSE (Apache-2.0, matched to pyproject.toml) + CITATION.cff. Commit `5068911` is local-only, **needs its own push go-ahead** — not assumed from the prior push. Next open: scanner-integration phase (#16: dlint/Pysa) for either agent; the missing `bola-client-supplied-owner-key` clean counterpart is a flagged future-work item, not in progress. | `corpus/*`, `CORPUS_METHODOLOGY.md`, `mcpbench/__init__.py` (Wilson CI), `tests/test_pipeline.py`, `LICENSE`, `CITATION.cff` | 9 commits total this session, 8 pushed + 1 local (`5068911`): `cf66939` (Wilson 95% CI), `ad069a6`/`5240d39`/`9e13d62` (8 new authz-logic cases + 3 clean), `e9baa63` (board+contract), `cdd59ed` (Codex: Semgrep fuller packs), `364117f`/`5f7cbc0` (Fade review notes), `619bbde` (Codex: README/board sync), `5068911` (Fade: real headline + adversarial verify + citability, **unpushed**). 19 cases / 10 distinct classes, reference 4/11 [15%,65%], semgrep+bandit 0/11 [0%,26%] (live CI), 0/6 and 1/6 false positives respectively. |
| Codex | vNext MCP authz corpus proposal | Operator approved proceeding with the first vNext lane on 2026-07-08. Took the **resource/audience boundary** slice from the TAC workspace patch plan: three new authz cases with clean counterparts, plus methodology/test/README updates. Local commit `bf68ca2` created; no push. | `corpus/resource-missing-accepted/`, `corpus/clean-resource-required/`, `corpus/foreign-audience-token-accepted/`, `corpus/clean-audience-validation/`, `corpus/resource-prefix-canonicalization-bypass/`, `corpus/clean-resource-canonicalization/`, `tests/test_pipeline.py`, `CORPUS_METHODOLOGY.md`, `README.md`, `BOARD.md` | READY FOR REVIEW — host-safe gates passed: `pytest` 4/4; local `mcpbench run` stayed reference-only, 1 scanner x 25 cases -> 5 findings; `mcpbench score` = reference 4/14 authz [12%,55%], 0/2 control, 0/9 FP. Disposable-CI Semgrep/Bandit/Dlint results pending; local commit exists, push remains gated. |

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
- 2026-06-30 — **Codex**: took the scanner-integration lane and landed the first narrow pass:
  Semgrep now runs the fuller methodology-promised registry packs (`p/python`, `p/secrets`,
  `p/owasp-top-ten`, `p/security-audit`) in `mcpbench/__init__.py`, and the CI diagnostic in
  `.github/workflows/scan.yml` mirrors the same command. No new dependency/scanner added yet. Local
  verification (host-safe: only the built-in reference scanner active here): `.venv/bin/python -m
  pytest tests/` = 4/4; `.venv/bin/mcpbench run` = 1 scanner [reference] x 19 cases -> 5 findings;
  `.venv/bin/mcpbench score` = reference 4/11 authz [15%,65%], 0/2 control, 0/6 FP. Semgrep result
  itself is intentionally left for the disposable GitHub Actions runner.
- 2026-06-30 — **Fade**: reviewed Codex's `cdd59ed` (operator: "codex is working now, give it a
  look"). Collision-checked first (board's own §1 rule) — found it already committed, not sitting
  uncommitted, so no hold/serialize needed. Read the full diff: purely additive Semgrep config
  inside the existing `semgrep_available()`-gated path, matches CORPUS_METHODOLOGY.md's own
  anti-p-hacking commitment word for word, stays inside the proposed scanner-integration lane,
  doesn't touch any Fade-owned file. **Independently re-ran everything rather than trust the
  numbers in Codex's own board entry** — PII gate 0, `pytest` 4/4, live `run`/`score` exact match
  (19 cases, reference 4/11=36% [15%,65%], 0/2 control, 0/6 FP). Clean. **Not pushed** — the
  operator's instruction was to look, not to push; that's still a separate, explicit call.
- 2026-06-30 — **Codex**: follow-up adversarial corpus/readme pass after Fade's review commit. The
  expanded-corpus cases keep the disclosure floor (new cases use abstract mechanism + CWE, no
  target/finding IDs) and the clean counterparts close their advertised gaps. `README.md` was stale:
  it still presented the old 8-case Semgrep/Bandit table as the current headline even though the
  branch now has 19 cases and fuller Semgrep packs. Updated README status to 19 cases, local
  host-safe reference score 4/11 authz with Wilson CI [15%,65%], and marked the old Semgrep/Bandit
  table as historical until disposable-CI reruns regenerate the public headline. Legacy
  `fastapi_mcp-*` labels remain only in the original cases and the methodology's explicit warning;
  leave/remove before push remains an operator/Fade judgment call, not changed by Codex.
- 2026-06-30 — **Fade**: reviewed Codex's `619bbde` (operator: "lets proceed to push"). Collision-
  checked first — already committed, working tree clean. Full diff is doc-only (README + this board),
  no corpus/methodology/scoring-code touched, matches its own board entry word for word. Independently
  re-verified rather than trust the entry: PII gate over the entire unpushed range `git diff
  origin/main..HEAD` = 0, `pytest` 4/4, live `run`/`score` exact match (19 cases, reference 4/11=36%
  [15%,65%], 0/2 control, 0/6 FP) — identical to README's new numbers. Checked all 8 unpushed commits:
  uniform pseudonym authorship (`StellarRequiem <stellarrequiem@users.noreply.github.com>`), no
  upstream divergence (`git log HEAD..origin/main` empty, clean fast-forward). **Pushed** —
  `git push origin main`, `72e62d4..619bbde`, confirmed `origin/main` == local `HEAD` post-push.
  Live: https://github.com/StellarRequiem/mcp-bench. Corpus is now 8→19 cases, public.
- 2026-06-30 — **Fade**: operator said "continue... accelerated pace." CI on the `619bbde` push had
  already completed (`ci` + `scan`, both green) — pulled the live `scan` artifact (run `28482069463`)
  rather than write speculative numbers: semgrep + bandit (fuller registry packs) score **0/11**
  authz-logic on the expanded corpus, a stronger result than the old 0/3. Before publishing that as
  the headline, ran a 4-way adversarial verification workflow (one reviewer per case bundle,
  explicitly briefed to find reasons the 0/11 claim might be weaker than it looks) — no disqualifying
  issues; every vulnerable case maps to a recognizable real bug class, every clean case genuinely
  closes its gap, one reviewer independently re-pulled the same CI artifact and got an identical
  result. Two honest caveats surfaced and are now disclosed in `CORPUS_METHODOLOGY.md`: (1) 11 cases
  span 10 distinct root-cause classes, not 11 independent trials (`unencoded-query-param-traversal`
  correlates with `op-filter-bypass`); (2) `bola-client-supplied-owner-key` has no clean counterpart
  yet. Fixed a cosmetic `vuln_line` pointer on `bola-missing-owner-filter` (comment line → actual
  predicate line; metadata-only, doesn't touch scoring, not a post-hoc rewrite). Also added
  `LICENSE` (Apache-2.0, matching the pre-existing `pyproject.toml` declaration — caught and fixed a
  near-miss where I'd first drafted MIT) and `CITATION.cff`. Re-verified: PII gate 0, `pytest` 4/4,
  live local `run`/`score` unchanged (4/11 reference, file-level scoring confirmed unaffected by the
  vuln_line fix). Committed `5068911`, pseudonym identity, **local only — held pending the operator's
  next explicit push go-ahead**, per AGENTS.md §5 (every push is its own decision, not inferred from
  momentum).
- 2026-06-30 — **Codex**: picked up the open scanner-integration lane after Fade's verified headline.
  Wired Dlint as a CI-only scanner subject: `parse_dlint()` normalizes Flake8/Dlint `DUO*` findings,
  `dlint_available()` requires both the `flake8` executable and the `dlint` package, and the scan
  workflow now installs `flake8 dlint` alongside Semgrep/Bandit plus a diagnostic control run. Pure
  parser sanity checked locally with a synthetic DUO line; no Dlint package is installed on this host,
  so the live local benchmark correctly stayed reference-only. Verification: `pytest` 4/4; live
  `mcpbench run` = 1 scanner [reference] x 19 cases -> 5 findings;
  `mcpbench score` unchanged at reference 4/11 authz [15%,65%], 0/2 control, 0/6 FP. Dlint's real
  result is deliberately left for disposable CI, not guessed locally.
- 2026-06-30 — **Fade**: reconciled a conversation↔disk desync (the operator rewound the chat; git and
  origin were ahead of this thread's memory). Independently re-verified the pre-rewind work via a
  3-agent workflow *before* trusting or pushing: (1) **adversarial** check of the public `5068911`
  "0/11 semgrep+bandit" headline — matches the raw CI artifact of run `28482069463` (commit `619bbde`)
  cell-for-cell, independently re-derived from `results.json`, reproduced byte-identical by a 2nd run
  (`28482832073`); the refutation attempt failed. (2) `c28aebc` dlint host-safety — `dlint_available()`
  gates on `shutil.which('flake8')` + `find_spec('dlint')`, both absent on host → never runs locally;
  CI-only install; mirrors the semgrep/bandit pattern exactly. (3) gate/provenance — PII 0 (both the
  full range and the public commit), pseudonym-only authorship, `pytest` 4/4, LICENSE Apache-2.0,
  CITATION pseudonymous. All **SOUND**. Then **pushed `c28aebc`** (operator: "continue pushing") —
  `4696d9d..c28aebc`, PII-gate 0 as a separate blocking step, clean fast-forward, `origin/main` ==
  local post-push. `5068911` was already public from the pre-rewind timeline and is now re-verified;
  origin is at `c28aebc`; **nothing left unpushed.**
- 2026-07-08 — **Codex**: operator approved proceeding with the TAC workspace's first vNext lane.
  Added the **resource/audience boundary** slice: `resource-missing-accepted`,
  `foreign-audience-token-accepted`, and `resource-prefix-canonicalization-bypass`, each with a clean
  counterpart. Updated methodology/tests/README to keep the old 19-case CI headline separate from the
  new 25-case local branch. Host-safe gates passed after sandbox write escalation for normal repo
  artifacts: `pytest` 4/4; local `mcpbench run` stayed reference-only, 1 scanner x 25 cases -> 5
  findings; `mcpbench score` = reference 4/14 authz [12%,55%], 0/2 control, 0/9 FP. No third-party
  scanners were run on host. Local commit `bf68ca2` created; no push yet.

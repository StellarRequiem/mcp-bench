# Corpus methodology (pre-registered before scoring any new scanner against the expanded corpus)

This file locks the rules for adding to `corpus/` *before* any new scanner run is scored against the
result, so the headline can't be tuned after seeing how a scanner performs. Dated by its commit, which
predates every case added under it.

## Abstraction rule

Every `authz-logic` case is generalized from a real, responsibly-confirmed finding, but is **rewritten
from scratch** -- never lifted verbatim, never reusing the real target's variable names, file layout,
route paths, or any other detail specific enough to identify it. `corpus/op-filter-bypass/server.py`
already follows this (compare its generic `ALLOWED = ("items", "users")` / `route()` shape to the real
finding it's modeled on) -- that's the template every new case follows, not a one-off.

**Disclosure floor, stricter than the existing precedent:** an existing case (`op-filter-bypass`)
labels itself `"(fastapi_mcp-001 class)"` in its `why` field, naming the real target package and an
internal finding ID. As of this methodology's commit, that finding is still unsubmitted and
undisclosed -- flagged to the operator as a standing judgment call worth re-examining, not silently
changed here. Every case added *after* this file does **not** name a target or finding ID. The `why`
field cites only the abstract vulnerability mechanism plus a CWE number; `source` stays the existing
generic `"generalized from a real responsibly-confirmed finding"` string, nothing more specific. If a
finding is later disclosed/patched, naming it retroactively is a deliberate, separate decision -- not
a default.

## Scoring rule (already implemented in `score()`, restated here so it can't silently drift)

A scanner "detects" a case iff it produced at least one finding where `case == <case id>` AND
`file == case["vuln_file"]` -- file-level granularity, not line number or vulnerability class. A
"false positive" is any finding at all on a `clean`-kind case's file. Both rules are fixed as of this
commit; changing them later is a methodology change, not a corpus change, and should be called out as
one in the commit that does it.

## Reference detector scope (honest, not padded)

`reference_scan` is explicitly a *naive*, hand-tuned heuristic over the original three authz-logic
classes (`operation-filter-bypass`, `fake-dcr-secret-leak`, `empty-filter-bypass`) -- it is not, and is
not claimed to be, a general authorization-bug detector. New authz-logic classes added under this
methodology are **not required** to extend `reference_scan` to catch them. Writing a pattern that
*only* matches a newly-added case's exact text would be circular (tuning the detector to the case
instead of the other way around) -- the honest state is "the reference detector doesn't yet cover this
class," reported as such, not silently inflated to 100% by hand-fitting a regex to one example.

## Corpus, as of this file's commit

| kind | class | reference covers it? |
|---|---|---|
| authz-logic | operation-filter-bypass | yes |
| authz-logic | fake-dcr-secret-leak | yes |
| authz-logic | empty-filter-bypass | yes |
| authz-logic | bola-missing-owner-filter | not yet |
| authz-logic | bola-client-supplied-owner-key | not yet |
| authz-logic | mass-assignment-upsert-takeover | not yet |
| authz-logic | unencoded-interpolation-traversal | not yet (a generalization test, not a new class for the reference detector) -- **statistically correlated with `operation-filter-bypass`, see note below, not an independent trial** |
| authz-logic | guard-divergence-across-paths | yes, incidentally -- see note below the table |
| authz-logic | list-call-surface-divergence | not yet |
| authz-logic | permissive-default-role | not yet |
| authz-logic | confused-deputy-forwarded-credential | not yet |
| authz-logic | missing-resource-indicator | not yet |
| authz-logic | foreign-audience-token-accepted | not yet |
| authz-logic | resource-prefix-canonicalization-bypass | not yet |

**Note on `guard-divergence-across-paths`:** this table originally predicted "not yet" before the
first live run. The actual run shows the naive `operation-filter-bypass` regex (an unparameterized
`\.replace\(.*\{.*\}` check with no canonical-encoding-function-name nearby) fires on this case's
*actual* vulnerable line (`build_url_legacy`, the unencoded sibling) -- a correct detection, for the
right reason. It also incidentally fires on the *safe* function's line, because that heuristic's
"is it encoded?" check only recognizes `quote(`/`urlencode`/`.encode`/`escape(` by name and doesn't
recognize the safe function's manual `.replace(".", "%2E")` percent-encoding as encoding at all. Both
findings collapse into a single case-level "detected" verdict under the file-level scoring rule, so
the case still passes correctly overall -- but the within-case false-positive-on-the-safe-line is a
real, minor limitation of the reference detector's narrow encoding heuristic, reported here rather
than fixed by editing the case (the case was not touched after this result was observed, per the
anti-p-hacking commitments below).
| control | hardcoded-secret | n/a (control, not authz-logic) |
| control | command-injection | n/a |
| clean | clean-filter / clean-dcr / clean-url-builder / clean-bola-owner / clean-mass-assignment / clean-list-call-divergence / clean-resource-required / clean-audience-validation / clean-resource-canonicalization | n/a |

## vNext resource/audience additions (2026-07-08)

The 2026-07-08 vNext slice adds three MCP resource/audience-boundary classes and one clean counterpart
for each:

- `resource-missing-accepted` / `clean-resource-required`
- `foreign-audience-token-accepted` / `clean-audience-validation`
- `resource-prefix-canonicalization-bypass` / `clean-resource-canonicalization`

These are generalized from official MCP authorization/resource-boundary guidance, not from a named
private target. They intentionally do **not** extend `reference_scan`; tuning the reference detector to
new exact fixtures would be circular. The local host-safe gate after adding them was:

- `pytest`: 4/4
- `mcpbench run`: 1 scanner `[reference]` x 25 cases -> 5 findings
- `mcpbench score`: reference 4/14 authz-logic [12%,55%], 0/2 control, 0/9 false positives

Semgrep, Bandit, and Dlint results for the expanded 25-case branch remain pending a disposable GitHub
Actions runner. Do not reuse the older 19-case CI headline as a 25-case result.

## Adversarial verification (2026-06-30)

Before the expanded-corpus headline shipped publicly, every new authz-logic and clean case was
independently re-reviewed by a fresh pass (4 parallel reviewers, one per case bundle, none of which
authored the cases) with an explicit brief to find reasons the eventual scanner-miss headline might be
weaker than it looks -- not to confirm it. Full findings are in the session record; the load-bearing
results:

- **No case was found to be uncatchable trivia, mislabeled, or a contrived non-bug.** Every vulnerable
  case maps to a recognizable real-world class (BOLA/CWE-639, mass assignment/CWE-915, path
  traversal/CWE-22, incomplete mediation/CWE-862, confused deputy/CWE-441, insecure default/CWE-1188,
  advertised-vs-dispatchable divergence/CWE-285) that a careful human reviewer would plausibly catch on
  inspection. `tool-list-call-divergence` and its clean counterpart were verified by direct code
  execution, not just by reading -- the bug and the fix both behave exactly as claimed.
- **Every clean case checked genuinely closes its paired gap** (symmetric owner-scoping, a real
  positive field allowlist, an unconditional prune) rather than superficially resembling a fix.
- **The 0/11 figure was independently re-derived from the live CI artifact** (GitHub Actions run
  `28482069463`, not the README's own prior claim) and confirmed to be zero findings of *any* class on
  all 11 authz-logic files -- ruling out a scoring-rule miscount -- while both control bugs were
  correctly caught and the one known bandit false positive (clean-dcr, `B105`) reproduced exactly.
- **Two honest limitations surfaced, neither disqualifying, both disclosed rather than hidden:**
  1. `unencoded-query-param-traversal` shares its root cause with the pre-existing `op-filter-bypass`
     case (same exploit shape, only the interpolation syntax differs) -- a scanner missing one will
     essentially always miss the other, so they are not independent draws. The corpus is therefore
     **11 cases across 10 distinct root-cause classes**, not 11 independent ones; a maximally rigorous
     reading of the Wilson CI should account for that correlation rather than treat n=11 as fully
     independent trials.
  2. `bola-client-supplied-owner-key` (the spoofable-parameter BOLA variant) has no paired clean case
     in the corpus, so its false-positive behavior is untested -- same disclosed-gap situation as
     `scope-elevation-via-default-role` and `confused-deputy-forwarded-credential`, which were always
     documented (commit `9e13d62`) as 3-of-8 deliberately paired, not an oversight.
- **Cosmetic-only fix applied as a result of this pass:** `bola-missing-owner-filter/case.json`'s
  `vuln_line` previously pointed at the explanatory `# VULN` comment (line 20) rather than the actual
  unscoped predicate (line 22). Corrected for precision. This does not change scoring (file-level, not
  line-level, per the rule above) or which case is vulnerable -- it is a metadata-accuracy fix, not a
  rewrite made after seeing a scanner result, so it does not violate the anti-p-hacking commitment below.

## Anti-p-hacking commitments

- No new authz-logic case is rewritten *after* seeing how a scanner scores against it. If a case
  accidentally gets caught by semgrep/bandit/a future scanner, that result ships as-is.
- Control-case edits aimed at making a scanner detect them are fine (controls are supposed to be the
  easy class); authz-logic-case edits aimed at making a scanner miss them are not, and none have been
  made.
- Before any new headline claim ships, semgrep is re-run against its full relevant default registry
  packs (`p/owasp-top-ten`, `p/security-audit`, in addition to the already-used `p/python` +
  `p/secrets`) -- an inconvenient catch from an untried default pack gets reported, not omitted.

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
| control | hardcoded-secret | n/a (control, not authz-logic) |
| control | command-injection | n/a |
| clean | clean-filter / clean-dcr / clean-url-builder / clean-bola-owner / clean-mass-assignment | n/a |

## Anti-p-hacking commitments

- No new authz-logic case is rewritten *after* seeing how a scanner scores against it. If a case
  accidentally gets caught by semgrep/bandit/a future scanner, that result ships as-is.
- Control-case edits aimed at making a scanner detect them are fine (controls are supposed to be the
  easy class); authz-logic-case edits aimed at making a scanner miss them are not, and none have been
  made.
- Before any new headline claim ships, semgrep is re-run against its full relevant default registry
  packs (`p/owasp-top-ten`, `p/security-audit`, in addition to the already-used `p/python` +
  `p/secrets`) -- an inconvenient catch from an untried default pack gets reported, not omitted.

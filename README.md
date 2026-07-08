# mcp-bench

**An independent, reproducible benchmark of how well MCP security scanners detect
*authorization-logic* vulnerabilities** — seeded with real, responsibly-confirmed findings.

Most MCP scanners are evaluated by their own authors, and existing benchmarks (MCPSecBench, MCPTox)
target prompt-injection / tool-poisoning at the config layer. mcp-bench asks the unanswered question:

> **Do the source/implementation scanners actually catch deep authorization-logic bugs** — broken
> object-level auth, confidential-secret exposure, operation-filter bypass — the class behind the real
> high-impact incidents?

It measures per-scanner **detection** and **false-positive** rates on a labeled corpus, reproducibly,
and reports the truth either way (a "scanners are good" result is equally valid).

**Scope:** source/implementation scanners only. Config-only scanners (manifest/prompt-injection
detectors) are a different tool for a different job and are explicitly out of scope — testing them on
source bugs would be a strawman.

## Quickstart
```sh
pip install -e .
mcpbench            # run every registered scanner over the corpus, then score
```

## Status

**Local vNext branch — 25 labeled cases:** 14 authorization-logic cases plus 2 control bugs and 9
clean negatives. The 2026-07-08 vNext slice adds three MCP resource/audience-boundary classes
(`missing-resource-indicator`, `foreign-audience-token-accepted`,
`resource-prefix-canonicalization-bypass`) with clean counterparts. These new cases have passed the
host-safe local gate (`pytest` 4/4; reference-only `mcpbench run`/`score`: 4/14 authz, 0/2 control,
0/9 false positives) but have **not yet been scored by disposable-CI Semgrep/Bandit/Dlint**, so they
do not change the CI-verified public scanner headline below.

**Last CI-verified expanded-corpus headline — 19 labeled cases:** 11 authorization-logic cases across **10 distinct root-cause
classes** (generalized from real, responsibly-confirmed findings under the disclosure rules in
`CORPUS_METHODOLOGY.md`; two cases share a root cause as a deliberate AST-generalization test, see the
methodology doc) · 2 control bugs a source scanner *should* catch (hardcoded secret, command
injection) · 6 clean negatives for false-positive measurement.

**Headline result** — semgrep (fuller registry packs: `p/python`, `p/secrets`, `p/owasp-top-ten`,
`p/security-audit`) and bandit, run in the disposable GitHub Actions sandbox against the full expanded
corpus ([live run](https://github.com/StellarRequiem/mcp-bench/actions/runs/28482069463), commit
`619bbde`):

| scanner | authz-logic | 95% CI | control | false-pos |
|---|---:|---:|---:|---:|
| **semgrep** (general SAST) | **0/11 (0%)** | [0%, 26%] | 2/2 (100%) | 0/6 |
| **bandit** (general SAST) | **0/11 (0%)** | [0%, 26%] | 2/2 (100%) | 1/6 |
| reference (our authz-logic detector) | 4/11 (36%) | [15%, 65%] | 0/2 (n/a — specialist) | 0/6 |

> **Last CI-verified 19-case result:** two independent mature general-purpose SASTs, run with their fuller default rule packs, still miss
> every authorization-logic case (0/11) while correctly catching both control bugs (2/2) and staying
> nearly false-positive-free (≤1/6)** — the control hit rate proves the tools are actually running, so
> the authz-logic miss is a real capability gap, not a setup artifact. This result was adversarially
> re-reviewed case-by-case before publication (see "Adversarial verification" in
> `CORPUS_METHODOLOGY.md`) — every vulnerable case maps to a recognizable real bug class a careful human
> reviewer would plausibly catch, and the headline number was independently re-derived from the raw CI
> artifact rather than trusted from a summary. One honest caveat: of the 11 cases, 2 share a root cause
> (an AST-shape generalization test, not a new class), so the *effective* class-level result is 0/10,
> not 11 fully independent trials — disclosed, not hidden, in the methodology doc. (bandit's 1 false
> positive — a `B105` string-heuristic flagging an OAuth `"none"` value near a token-named key in a
> *clean* case — is the same known cause as the original v1 corpus; reported, not omitted.)

## Historical v1 Baseline
**v1 corpus — 8 labeled cases:** 3 authorization-logic (all real, responsibly-confirmed finds:
operation-filter bypass, fake-DCR secret leak, empty-filter bypass) · 2 control bugs · 3 clean
negatives.

**Historical headline result** (semgrep + bandit, run in the disposable CI sandbox — see below):

| scanner | authz-logic | control | false-pos |
|---|---|---|---|
| **semgrep** (general SAST) | **0/3 (0%)** | 2/2 (100%) | 0/3 |
| **bandit** (general SAST) | **0/3 (0%)** | 2/2 (100%) | 1/3 |
| reference (our authz-logic detector) | 3/3 (100%) | 0/2 (n/a — specialist) | 0/3 |

> **Historical v1 result:** two independent mature general-purpose SASTs each catch the
> easy/generic classes (controls 2/2)
> yet are blind to the authorization-logic class (0/3)** — empirical support for the thesis across
> scanners, not a single-tool quirk. The control 2/2 proves they *work*, so the authz-logic miss is
> meaningful, not a setup artifact. (bandit's 1 false-positive — a `B105` string-heuristic flagging an
> OAuth `"none"` value near a token-named key in a *clean* case — is itself honest signal: general SAST
> is noisier; we report it rather than hide it.)

**Isolation:** scanners are untrusted third-party code, so they run **only inside a disposable sandbox
— the GitHub Actions ephemeral runner (`.github/workflows/scan.yml`), never a developer host.** Local
runs + the test suite are host-safe (the reference detector is our own code; semgrep runs only where
installed, i.e. in CI).

## Methodology

The scoring rule, abstraction rule, disclosure floor, and anti-p-hacking commitments are pre-registered
in [`CORPUS_METHODOLOGY.md`](./CORPUS_METHODOLOGY.md) — locked before any new scanner is scored against
an expanded corpus, so the headline can't be tuned after the fact. Every detection-rate figure above
carries a 95% Wilson confidence interval, not a bare percentage, because a small-N rate alone overstates
precision.

## License & Citation

Apache License 2.0 — see [`LICENSE`](./LICENSE). If you use mcp-bench, see
[`CITATION.cff`](./CITATION.cff) for citation metadata.

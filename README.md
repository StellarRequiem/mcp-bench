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
**Expanded corpus — 19 labeled cases:** 11 authorization-logic cases (generalized from real,
responsibly-confirmed findings under the disclosure rules in `CORPUS_METHODOLOGY.md`) · 2 control
bugs a source scanner *should* catch (hardcoded secret, command injection) · 6 clean negatives for
false-positive measurement.

The local, host-safe sanity check currently runs only the built-in reference detector:

| scanner | authz-logic | 95% CI | control | false-pos |
|---|---:|---:|---:|---:|
| reference (our authz-logic detector) | 4/11 (36%) | [15%, 65%] | 0/2 (n/a — specialist) | 0/6 |

The general-SAST headline for semgrep and bandit must be regenerated in the disposable GitHub
Actions runner before publication. In particular, semgrep is now configured to run the fuller
methodology-promised registry packs (`p/python`, `p/secrets`, `p/owasp-top-ten`,
`p/security-audit`), so the older 8-case numbers below are historical only, not the current headline.

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

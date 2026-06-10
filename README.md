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
**v1 corpus complete — 8 labeled cases:** 3 authorization-logic (all real, responsibly-confirmed
finds: operation-filter bypass, fake-DCR secret leak, empty-filter bypass) · 2 control bugs a source
scanner *should* catch (hardcoded secret, command injection) · 3 clean negatives (per-class
false-positive measurement).

**Headline result** (semgrep 1.x, run in the disposable CI sandbox — see below):

| scanner | authz-logic | control | false-pos |
|---|---|---|---|
| **semgrep** (general SAST) | **0/3 (0%)** | **2/2 (100%)** | 0/3 |
| reference (our authz-logic detector) | 3/3 (100%) | 0/2 (n/a — specialist) | 0/3 |

> A mature general-purpose SAST **catches the easy/generic classes (controls 2/2) yet is blind to the
> authorization-logic class (0/3)** — empirical support for the thesis, with **zero false-positives**.
> The control 2/2 proves semgrep *works*, so its authz-logic miss is meaningful, not a setup artifact.

**Isolation:** scanners are untrusted third-party code, so they run **only inside a disposable sandbox
— the GitHub Actions ephemeral runner (`.github/workflows/scan.yml`), never a developer host.** Local
runs + the test suite are host-safe (the reference detector is our own code; semgrep runs only where
installed, i.e. in CI).

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
false-positive measurement). A multi-class reference detector proves the measurement frame
(authz-logic 3/3, control 0/2 by design, **0 false-positives**), CI-green from a clean clone.

**Next phase — gated on isolation:** wiring real third-party scanner adapters. Scanners are untrusted
third-party code, so they run **only inside a disposable sandbox (container/VM), never the host.**

# Security Policy

Thank you for helping keep `mcp-bench` safe and accurate.

`mcp-bench` is a defensive benchmark for MCP/source authorization-logic scanner capability. Some corpus fixtures intentionally model vulnerable patterns so scanners can be evaluated. Please do not report an intentionally vulnerable fixture as a project vulnerability unless the issue affects the benchmark tool, packaging, runner, methodology, or published results.

## Supported Versions

The active `main` branch is the supported branch unless this policy is updated.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately through:

- GitHub private vulnerability reporting, if enabled for this repository.
- If private vulnerability reporting is unavailable, open a non-sensitive issue requesting a private coordination channel. Do not post sensitive vulnerability details publicly.

Useful reports include:

- Unsafe scanner execution or sandbox escape risks.
- Dependency, artifact, or CI handling issues.
- Misleading benchmark scoring or result integrity problems.
- Disclosure-floor violations in a corpus case.
- Vulnerabilities in benchmark tooling rather than intentionally vulnerable fixtures.

Please include the affected commit, a concise description, impact, and minimal reproduction details. Do not include unrelated secrets, tokens, private third-party data, or embargoed vulnerability details.

## Coordinated Disclosure

Please do not publicly disclose a vulnerability until there has been a reasonable chance to triage and remediate it. If the report affects a third-party scanner or upstream project, coordination with that maintainer may be needed.

## Safe Harbor Intent

Good-faith research is welcome when it stays within the project scope, avoids privacy violations and disruption, and uses local reproduction where possible. Activity outside those boundaries is not authorized by this policy.

## Project-Specific Notes

- Corpus cases may intentionally contain vulnerable code patterns.
- Third-party scanners should run only in disposable CI/sandbox contexts, not on a maintainer host.
- Benchmark claims should preserve caveats, confidence intervals, and disclosure-floor rules.

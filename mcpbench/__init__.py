"""mcp-bench — an independent, reproducible benchmark of how well MCP security scanners detect
*authorization-logic* vulnerabilities, seeded with real responsibly-confirmed finds.

Walking skeleton (G2): a REAL built-in reference detector runs the REAL corpus end-to-end through
run -> score, producing real detection + false-positive numbers. Third-party scanner adapters
(CSA mcpserver-audit, mcp-security-auditor, Snyk agent-scan) plug into the same `SCANNERS` registry
next (G3). Nothing here is mocked — the detector genuinely reads each case's source.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
RESULTS = ROOT / "results.json"


def load_cases():
    out = []
    for d in sorted(p for p in CORPUS.iterdir() if (p / "case.json").is_file()):
        c = json.loads((d / "case.json").read_text(encoding="utf-8"))
        c["name"] = d.name
        c["dir"] = d
        out.append(c)
    return out


# --------------------------------------------------------------------------- #
# Scanners. A scanner is name -> scan(case_dir, name) -> [finding dicts].
# The reference detector is a real (deliberately naive) static check for the operation-filter-bypass
# class: a request path/URL built by string substitution WITHOUT percent-encoding — the exact pattern
# behind fastapi_mcp-001, where a crafted operation id traverses the operation filter.
# --------------------------------------------------------------------------- #
def reference_scan(case_dir, name="reference"):
    findings = []
    src = case_dir / "server.py"
    if not src.is_file():
        return findings
    for i, line in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        cls = None
        builds_path = re.search(r"\.replace\(.*\{.*\}", line) or re.search(r"(path|url)\s*=.*\{[a-z_]+\}", line, re.I)
        encoded = any(tok in line for tok in ("quote(", "urlencode", ".encode", "escape("))
        if builds_path and not encoded:
            cls = "operation-filter-bypass"                          # unencoded path substitution
        elif re.search(r'["\']client_secret["\']\s*:', line):
            cls = "fake-dcr-secret-leak"                             # confidential secret echoed in a response
        elif re.search(r"not\s+\w*filter\w*\s+or\b", line, re.I):
            cls = "empty-filter-bypass"                              # empty filter degrades to allow-all
        if cls:
            findings.append({"scanner": name, "case": case_dir.name, "cls": cls, "file": "server.py", "line": i})
    return findings


SCANNERS = {"reference": reference_scan}


def run():
    cases = load_cases()
    results = [f for name, scan in SCANNERS.items() for c in cases for f in scan(c["dir"], name)]
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  ran {len(SCANNERS)} scanner(s) x {len(cases)} cases -> {len(results)} findings -> results.json")
    return results


def score(results=None):
    cases = load_cases()
    results = results if results is not None else json.loads(RESULTS.read_text(encoding="utf-8"))
    authz = [c for c in cases if c["kind"] == "authz-logic"]
    control = [c for c in cases if c["kind"] == "control"]
    clean = [c for c in cases if c["kind"] == "clean"]
    table = {}
    print(f"  corpus: {len(authz)} authz-logic + {len(control)} control + {len(clean)} clean")
    print(f"  {'scanner':12}{'authz-logic':>16}{'control':>14}{'false-pos':>12}")
    for name in SCANNERS:
        f = [r for r in results if r["scanner"] == name]

        def det(group):
            return sum(any(r["case"] == c["name"] and r["cls"] == c["class"] and r["file"] == c["vuln_file"] for r in f) for c in group)

        da, dc = det(authz), det(control)
        fp = sum(any(r["case"] == c["name"] for r in f) for c in clean)
        table[name] = {"detected": da, "authz_total": len(authz), "control_detected": dc,
                       "control_total": len(control), "fp": fp, "clean_total": len(clean)}
        ar = f"{da}/{len(authz)} = {da * 100 // max(len(authz), 1)}%"
        cr = f"{dc}/{len(control)} = {dc * 100 // max(len(control), 1)}%"
        print(f"  {name:12}{ar:>16}{cr:>14}{str(fp) + '/' + str(len(clean)):>12}")
    return table


def main():
    ap = argparse.ArgumentParser(prog="mcpbench", description="MCP scanner authz-logic detection benchmark")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("run", help="run every scanner over the corpus -> results.json")
    sub.add_parser("score", help="score results.json -> detection + FP table")
    args = ap.parse_args()
    if args.cmd == "run":
        run()
    elif args.cmd == "score":
        score()
    else:
        score(run())

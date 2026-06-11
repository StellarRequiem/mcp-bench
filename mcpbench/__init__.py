"""mcp-bench — an independent, reproducible benchmark of how well MCP security scanners detect
*authorization-logic* vulnerabilities, seeded with real responsibly-confirmed finds.

Scanners are UNTRUSTED third-party code, so real scanners run only inside a disposable, isolated
runner — the GitHub Actions ephemeral VM (see .github/workflows/scan.yml) — never on a primary host.
The built-in `reference` detector is our own code and runs anywhere. A scanner is invoked only if it
is actually available on the machine (`semgrep` runs where semgrep is installed — i.e. in CI), so the
local test suite stays host-safe.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
RESULTS = ROOT / "results.json"


def load_cases():
    out = []
    for d in sorted(p for p in CORPUS.iterdir() if (p / "case.json").is_file()):
        c = json.loads((d / "case.json").read_text(encoding="utf-8"))
        c["name"], c["dir"] = d.name, d
        out.append(c)
    return out


# ----- reference detector: our own code, real but deliberately naive, runs anywhere -----
def reference_available():
    return True


def reference_scan(case_dir, name="reference"):
    findings, src = [], case_dir / "server.py"
    if not src.is_file():
        return findings
    for i, line in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        cls = None
        builds_path = re.search(r"\.replace\(.*\{.*\}", line) or re.search(r"(path|url)\s*=.*\{[a-z_]+\}", line, re.I)
        encoded = any(tok in line for tok in ("quote(", "urlencode", ".encode", "escape("))
        if builds_path and not encoded:
            cls = "operation-filter-bypass"
        elif re.search(r'["\']client_secret["\']\s*:', line):
            cls = "fake-dcr-secret-leak"
        elif re.search(r"not\s+\w*filter\w*\s+or\b", line, re.I):
            cls = "empty-filter-bypass"
        if cls:
            findings.append({"scanner": name, "case": case_dir.name, "cls": cls, "file": "server.py", "line": i})
    return findings


# ----- semgrep: a real, mature general-purpose SAST baseline; runs only where installed (CI) -----
def parse_sarif(sarif, case_name, scanner):
    """Pure SARIF -> normalized findings. Testable without running the scanner."""
    out = []
    for run_ in sarif.get("runs", []):
        for res in run_.get("results", []):
            for loc in res.get("locations", []):
                phys = loc.get("physicalLocation", {})
                uri = phys.get("artifactLocation", {}).get("uri", "")
                ln = phys.get("region", {}).get("startLine", 0)
                out.append({"scanner": scanner, "case": case_name, "cls": res.get("ruleId", scanner),
                            "file": uri.split("/")[-1], "line": ln})
    return out


def semgrep_available():
    return shutil.which("semgrep") is not None


def semgrep_scan(case_dir, name="semgrep"):
    src = case_dir / "server.py"
    if not src.is_file():
        return []
    try:
        # concrete public rule-packs (no token needed); `auto` loads nothing without a Semgrep account
        out = subprocess.run(["semgrep", "scan", "--sarif", "--quiet",
                              "--config", "p/python", "--config", "p/secrets", str(src)],
                             capture_output=True, text=True, timeout=300)
        return parse_sarif(json.loads(out.stdout or "{}"), case_dir.name, name)
    except Exception:
        return []


# ----- bandit: a second mature general-purpose Python SAST baseline; runs only where installed (CI) -----
def parse_bandit(report, case_name, scanner):
    """Pure bandit-JSON -> normalized findings. Testable without running the scanner."""
    out = []
    for r in report.get("results", []):
        out.append({"scanner": scanner, "case": case_name, "cls": r.get("test_id", scanner),
                    "file": str(r.get("filename", "")).split("/")[-1], "line": r.get("line_number", 0)})
    return out


def bandit_available():
    return shutil.which("bandit") is not None


def bandit_scan(case_dir, name="bandit"):
    src = case_dir / "server.py"
    if not src.is_file():
        return []
    try:
        out = subprocess.run(["bandit", "-f", "json", "-q", str(src)],
                             capture_output=True, text=True, timeout=300)
        return parse_bandit(json.loads(out.stdout or "{}"), case_dir.name, name)
    except Exception:
        return []


# NOTE on CodeQL (attempted 2026-06-10, reverted): CodeQL runs cleanly here (verified: 174 queries
# evaluated, results interpreted) but finds NOTHING on this corpus — its default security suite targets
# REMOTE (network) taint sources, while our minimal controls use a LOCAL source (sys.argv) + a syntactic
# shell=True that semgrep/bandit catch syntactically but CodeQL's remote-taint queries don't flag. A
# verified null, but not a clean "works-then-misses-authz" signal. To re-include CodeQL, add a control
# with a REMOTE source (e.g. a FastAPI request param -> os.system) that py/command-line-injection fires on.
SCANNERS = {
    "reference": (reference_available, reference_scan),
    "semgrep": (semgrep_available, semgrep_scan),
    "bandit": (bandit_available, bandit_scan),
}


def active():
    return {n: sc for n, (av, sc) in SCANNERS.items() if av()}


def run():
    cases, act = load_cases(), active()
    results = [f for n, sc in act.items() for c in cases for f in sc(c["dir"], n)]
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  ran {len(act)} scanner(s) [{', '.join(act) or 'none'}] x {len(cases)} cases -> {len(results)} findings")
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
    for name in active():
        f = [r for r in results if r["scanner"] == name]
        det = lambda g: sum(any(r["case"] == c["name"] and r["file"] == c["vuln_file"] for r in f) for c in g)  # noqa: E731
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
    sub.add_parser("run")
    sub.add_parser("score")
    args = ap.parse_args()
    score(run()) if args.cmd not in ("run", "score") else (run() if args.cmd == "run" else score())

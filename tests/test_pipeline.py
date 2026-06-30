"""G2 It-Lives test: the pipeline runs end-to-end on the real corpus and the reference detector
genuinely discriminates the vulnerable case from the clean one (no mock)."""
from mcpbench import load_cases, run, score, wilson_ci


def test_corpus_loads():
    cases = load_cases()
    assert any(c["kind"] == "authz-logic" for c in cases), "need at least one authz-logic case"
    assert any(c["kind"] == "clean" for c in cases), "need at least one clean negative"


# The reference detector is an explicitly naive heuristic hand-tuned to ONLY these three classes
# (see CORPUS_METHODOLOGY.md "Reference detector scope") -- it is not claimed to generalize to every
# authz-logic case in the corpus, so this test scopes its 100%-detection assertion to what it actually
# covers rather than asserting a blanket "all authz_total cases", which would silently break (or
# require hand-fitting a regex to one example) every time a new, not-yet-covered class is added.
REFERENCE_COVERED_CLASSES = {"operation-filter-bypass", "fake-dcr-secret-leak", "empty-filter-bypass"}


def test_reference_detects_vuln_not_clean():
    cases = load_cases()
    table = score(run())
    r = table["reference"]
    covered = [c for c in cases if c["kind"] == "authz-logic" and c["class"] in REFERENCE_COVERED_CLASSES]
    assert len(covered) == len(REFERENCE_COVERED_CLASSES), "the three originally-covered classes must still exist in the corpus"
    f = [x for x in run() if x["scanner"] == "reference"]
    for c in covered:
        assert any(x["case"] == c["name"] and x["file"] == c["vuln_file"] for x in f), \
            f"reference detector must still catch its originally-covered class: {c['class']}"
    assert r["fp"] == 0, "reference detector must not false-positive on any clean case"
    assert r["authz_ci95"][0] <= r["detected"] / r["authz_total"] <= r["authz_ci95"][1]


def test_expanded_corpus_structure():
    """Honest-count check for the Phase-2 hardening batch: confirms the new cases actually loaded
    with the right kind/class/file wiring, independent of whether any scanner (reference included)
    catches them yet."""
    cases = {c["id"]: c for c in load_cases()}
    new_authz = ["bola-missing-owner-filter", "bola-client-supplied-owner-key", "mass-assignment-upsert-takeover",
                 "unencoded-query-param-traversal", "version-pinned-authz-divergence", "tool-list-call-divergence"]
    new_clean = ["clean-bola-owner", "clean-mass-assignment", "clean-list-call-divergence"]
    for cid in new_authz:
        assert cases[cid]["kind"] == "authz-logic"
        assert cases[cid]["vuln_file"] == "server.py"
        assert (cases[cid]["dir"] / cases[cid]["vuln_file"]).is_file()
        assert "VULN" in (cases[cid]["dir"] / "server.py").read_text()
        # disclosure floor: no target/finding-id naming in the new cases' rationale (CVE numbers are
        # exempt -- they're public identifiers, not new disclosures)
        assert "autogen" not in cases[cid]["why"].lower()
        assert "fastapi_mcp-0" not in cases[cid]["why"].lower()
    for cid in new_clean:
        assert cases[cid]["kind"] == "clean"
        assert cases[cid]["vuln_file"] is None


def test_wilson_ci_known_values():
    # 0/3 at 95% -> roughly [0%, 56%] (hand-verified against the textbook Wilson score formula);
    # this is the exact number that makes a thin-sample "0%" headline honest rather than overclaimed.
    lo, hi = wilson_ci(0, 3)
    assert lo == 0.0
    assert 0.55 < hi < 0.57
    # a wider corpus tightens the interval at the same observed rate
    lo12, hi12 = wilson_ci(0, 12)
    assert hi12 < hi, "more data must narrow the interval, not widen it"
    # zero-total guard: never divide by zero on an empty class
    assert wilson_ci(0, 0) == (0.0, 0.0)
    # a perfect detector's interval must still sit at/near 100%, never overflow past it
    lo_perfect, hi_perfect = wilson_ci(3, 3)
    assert hi_perfect <= 1.0
    assert lo_perfect > 0.4

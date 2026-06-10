"""G2 It-Lives test: the pipeline runs end-to-end on the real corpus and the reference detector
genuinely discriminates the vulnerable case from the clean one (no mock)."""
from mcpbench import load_cases, run, score


def test_corpus_loads():
    cases = load_cases()
    assert any(c["kind"] == "authz-logic" for c in cases), "need at least one authz-logic case"
    assert any(c["kind"] == "clean" for c in cases), "need at least one clean negative"


def test_reference_detects_vuln_not_clean():
    table = score(run())
    r = table["reference"]
    assert r["authz_total"] >= 1
    assert r["detected"] == r["authz_total"], "reference detector must catch the authz-logic case(s)"
    assert r["fp"] == 0, "reference detector must not false-positive on the clean case"

"""G2 It-Lives test: the pipeline runs end-to-end on the real corpus and the reference detector
genuinely discriminates the vulnerable case from the clean one (no mock)."""
from mcpbench import load_cases, run, score, wilson_ci


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
    assert r["authz_ci95"][0] <= r["detected"] / r["authz_total"] <= r["authz_ci95"][1]


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

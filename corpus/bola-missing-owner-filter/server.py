"""Minimal record store -- carries a broken object-level authorization vulnerability (CWE-639):
one accessor filters by owner, a sibling accessor for a different resource type does not. The
asymmetry is the point -- a scanner able to diff filter shapes across functions in the same file
has a real shot at this; one that pattern-matches a single function in isolation does not."""

SESSIONS = [{"id": 1, "user_id": "alice", "data": "alice's session"},
            {"id": 2, "user_id": "bob", "data": "bob's session"}]
RUNS = [{"id": 1, "user_id": "alice", "result": "alice's run output"},
        {"id": 2, "user_id": "bob", "result": "bob's run output"}]


def get_session(session_id, user_id):
    for s in SESSIONS:
        if s["id"] == session_id and s["user_id"] == user_id:   # scoped: id AND owner
            return s
    return None


def get_run(run_id):
    # VULN: no user_id predicate -- any caller reads any user's run by enumerable id (BOLA)
    for r in RUNS:
        if r["id"] == run_id:
            return r
    return None

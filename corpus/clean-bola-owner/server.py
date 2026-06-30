"""Clean negative / counterpart to bola-missing-owner-filter: both accessors filter by id AND
owner. A finding here is a false positive."""

SESSIONS = [{"id": 1, "user_id": "alice", "data": "alice's session"}]
RUNS = [{"id": 1, "user_id": "alice", "result": "alice's run output"}]


def get_session(session_id, user_id):
    for s in SESSIONS:
        if s["id"] == session_id and s["user_id"] == user_id:
            return s
    return None


def get_run(run_id, user_id):
    for r in RUNS:
        if r["id"] == run_id and r["user_id"] == user_id:   # scoped: id AND owner, same as get_session
            return r
    return None

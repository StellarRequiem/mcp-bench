"""Clean negative / counterpart to mass-assignment-upsert-takeover: the target is resolved by id
AND owner, and only an explicit allowlist of fields is ever written back -- the ownership column can
never be touched by the request body. A finding here is a false positive."""

SETTINGS = [{"id": 1, "user_id": "alice", "api_key": "sk-alice-secret"}]
WRITABLE_FIELDS = ("api_key",)


def update_settings(body, caller_user_id):
    target = None
    for s in SETTINGS:
        if s["id"] == body["id"] and s["user_id"] == caller_user_id:   # scoped by id AND owner
            target = s
            break
    if target is None:
        return None
    for k, v in body.items():
        if k in WRITABLE_FIELDS:    # only an explicit allowlist is ever written -- no ownership takeover
            target[k] = v
    return target

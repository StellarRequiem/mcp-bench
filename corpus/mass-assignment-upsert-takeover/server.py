"""Settings updater -- carries a write-side mass-assignment / authorization-bypass vulnerability
(CWE-915): the target row is resolved by a body-supplied id with no owner check, then every field in
the body is written back, including the ownership column itself -- so a caller can both retarget the
write at someone else's row and overwrite who owns it afterward."""

SETTINGS = [{"id": 1, "user_id": "alice", "api_key": "sk-alice-secret"}]


def update_settings(body):
    target = None
    for s in SETTINGS:
        if s["id"] == body["id"]:          # resolved by attacker-supplied id, no owner check
            target = s
            break
    if target is None:
        return None
    # VULN: every body field is written back, including user_id -- mass assignment / ownership takeover
    for k, v in body.items():
        target[k] = v
    return target

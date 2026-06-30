"""Settings accessor -- carries a subtler broken object-level authorization variant (CWE-639): a
scoping key is present, but it comes straight from caller-supplied input rather than an
authenticated session identity, so the filter exists syntactically but authorizes nothing. A naive
"is there a filter at all" check passes this case -- that is exactly the gap it is meant to probe."""

SETTINGS = [{"user_id": "alice", "api_key": "sk-alice-secret"},
            {"user_id": "bob", "api_key": "sk-bob-secret"}]


def get_settings(user_id):
    # VULN: user_id is attacker-controlled input, never bound to the authenticated caller's identity
    for s in SETTINGS:
        if s["user_id"] == user_id:
            return s
    return None

"""Internal proxy -- forwards the caller's own authorization header to an upstream internal target.
The destination is checked against a list of valid internal hosts, but never against which hosts
THIS caller is actually permitted to reach -- so any caller who can name a valid host gets the
proxy's elevated trust applied to credentials/auth headers regardless of their own permission scope
(a confused-deputy pattern, CWE-441)."""

INTERNAL_HOSTS = ("payments.internal", "users.internal", "admin-console.internal")


def proxy_request(caller_auth_header: str, caller_scope: list, target_host: str, path: str) -> dict:
    if target_host not in INTERNAL_HOSTS:        # checks the host is KNOWN...
        raise ValueError("unknown host")
    # VULN: caller_scope (what THIS caller may reach) is never consulted -- any caller who names a
    # valid internal host gets the proxy's own trust + the caller's forwarded header applied to it
    return {"forwarded_to": target_host, "path": path, "Authorization": caller_auth_header}

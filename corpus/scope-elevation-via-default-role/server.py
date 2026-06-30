"""Action authorizer -- a role check whose default value is permissive rather than safe, so simply
omitting the field silently elevates privilege (CWE-862 / CWE-1188, insecure default). A different
code idiom than the corpus's existing empty-filter-bypass (a dict.get default, not a
falsy-collection-or fallback)."""

PRIVILEGED_ACTIONS = ("delete_all", "reset_billing", "grant_admin")


def authorize_action(request: dict, action: str) -> bool:
    # VULN: omitting "role" defaults to "admin" -- the permissive default, not a safe one
    role = request.get("role", "admin")
    if action in PRIVILEGED_ACTIONS:
        return role == "admin"
    return True

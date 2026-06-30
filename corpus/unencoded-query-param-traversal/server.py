"""Resource fetcher -- the same unencoded-interpolation-into-a-path root cause as the corpus's
existing operation-filter-bypass case (CWE-22), but built with f-string interpolation rather than
.replace() substitution. Tests whether a scanner's detection generalizes across a structurally
equivalent but syntactically different AST shape, or is narrowly pattern-matched to one form."""

ALLOWED = ("items", "users")


def fetch_resource(resource: str, resource_id: str) -> str:
    if resource not in ALLOWED:                       # the filter checks the resource...
        raise PermissionError("resource not allowed")
    # VULN: f-string interpolation, no quote()/percent-encoding -- same traversal class as
    # operation-filter-bypass, different syntax shape (escapes the filter via "../" in resource_id)
    return f"/api/{resource}/{resource_id}"

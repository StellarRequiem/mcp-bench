"""Clean negative for resource-prefix-canonicalization-bypass: canonical resource comparison is
exact, so sibling paths do not inherit the MCP server's authorization boundary."""

from urllib.parse import urlsplit, urlunsplit

EXPECTED_RESOURCE = "https://mcp.example.test/mcp"


def canonical_resource(resource: str) -> str:
    parsed = urlsplit(resource.strip())
    if parsed.fragment:
        raise PermissionError("fragments are not valid resource identifiers")
    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or ""
    return urlunsplit((scheme, host, path, "", ""))


def authorize_request(auth_request: dict) -> str:
    if canonical_resource(auth_request.get("resource", "")) != EXPECTED_RESOURCE:
        raise PermissionError("wrong resource")
    return "authorized"

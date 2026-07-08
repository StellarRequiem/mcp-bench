"""MCP OAuth resource indicator is optional in this toy issuer even though the protected
resource must be named before a token can be safely scoped to an MCP server. CWE-862."""

EXPECTED_RESOURCE = "https://mcp.example.test/mcp"


def issue_access_token(auth_request: dict) -> dict:
    resource = auth_request.get("resource")
    if resource is not None and resource != EXPECTED_RESOURCE:
        raise PermissionError("wrong resource")
    # VULN: a missing resource silently turns into a wildcard token instead of a rejected request
    return {"aud": resource or "*", "scope": auth_request.get("scope", "tools:read")}


def read_tool_catalog(token: dict) -> list[str]:
    if "tools:read" not in token.get("scope", "").split():
        raise PermissionError("insufficient scope")
    return ["search", "summarize"]

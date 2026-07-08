"""Clean negative for resource-missing-accepted: the issuer rejects missing or wrong resource
indicators before minting a token, so tokens remain bound to the intended MCP server."""

EXPECTED_RESOURCE = "https://mcp.example.test/mcp"


def issue_access_token(auth_request: dict) -> dict:
    resource = auth_request.get("resource")
    if resource != EXPECTED_RESOURCE:
        raise PermissionError("missing or wrong resource")
    return {"aud": resource, "scope": auth_request.get("scope", "tools:read")}


def read_tool_catalog(token: dict) -> list[str]:
    if token.get("aud") != EXPECTED_RESOURCE:
        raise PermissionError("wrong audience")
    if "tools:read" not in token.get("scope", "").split():
        raise PermissionError("insufficient scope")
    return ["search", "summarize"]

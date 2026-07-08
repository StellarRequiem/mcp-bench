"""Clean negative for foreign-audience-token-accepted: issuer, audience, and scope are all
checked before the MCP resource server authorizes a tool call."""

EXPECTED_AUDIENCE = "https://mcp.example.test/mcp"
TRUSTED_ISSUER = "https://issuer.example.test"


def authorize_tool_call(token: dict, tool_name: str) -> str:
    if token.get("iss") != TRUSTED_ISSUER:
        raise PermissionError("untrusted issuer")
    if token.get("aud") != EXPECTED_AUDIENCE:
        raise PermissionError("wrong audience")
    if "tools:read" not in token.get("scope", "").split():
        raise PermissionError("insufficient scope")
    return f"allowed:{tool_name}"

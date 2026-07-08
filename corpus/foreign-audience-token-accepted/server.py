"""MCP resource server validates issuer and scope but forgets that access tokens must be
intended for this resource server. CWE-863."""

EXPECTED_AUDIENCE = "https://mcp.example.test/mcp"
TRUSTED_ISSUER = "https://issuer.example.test"


def authorize_tool_call(token: dict, tool_name: str) -> str:
    if token.get("iss") != TRUSTED_ISSUER:
        raise PermissionError("untrusted issuer")
    if "tools:read" not in token.get("scope", "").split():
        raise PermissionError("insufficient scope")
    # VULN: token["aud"] is never compared with EXPECTED_AUDIENCE before authorizing the call
    return f"allowed:{tool_name}"

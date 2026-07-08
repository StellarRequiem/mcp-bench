"""Weak resource canonicalization treats a sibling path as if it were the intended MCP resource.
CWE-863."""

EXPECTED_RESOURCE = "https://mcp.example.test/mcp"


def normalize_resource(resource: str) -> str:
    return resource.strip().lower().rstrip("/")


def authorize_request(auth_request: dict) -> str:
    resource = normalize_resource(auth_request.get("resource", ""))
    # VULN: prefix matching accepts https://mcp.example.test/mcp-admin as if it were /mcp
    if not resource.startswith(EXPECTED_RESOURCE):
        raise PermissionError("wrong resource")
    return "authorized"

"""Minimal MCP OAuth dynamic-client-registration (DCR) endpoint — carries the fake-DCR secret-leak
vulnerability (the fastapi_mcp-002 class). The /register endpoint echoes a confidential client_secret
back to ANY unauthenticated caller, so anyone who can reach it obtains the credential the MCP server
uses to authenticate to its upstream OAuth provider (confidential-client compromise)."""


def register(request_body: dict) -> dict:
    client_id = "mcp-" + request_body.get("client_name", "anon")
    client_secret = "confidential-" + client_id      # the credential that must stay secret
    # VULN: client_secret returned to an unauthenticated caller (no auth gate on /register)
    return {"client_id": client_id, "client_secret": client_secret, "grant_types": ["authorization_code"]}

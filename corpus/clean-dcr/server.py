"""Patched DCR /register — issues a PUBLIC client (token_endpoint_auth_method "none"); no confidential
secret is ever returned. Clean negative / counterpart to fake-dcr-secret-leak. A finding here is a
false positive."""


def register(request_body: dict) -> dict:
    client_id = "mcp-" + request_body.get("client_name", "anon")
    return {"client_id": client_id, "token_endpoint_auth_method": "none", "grant_types": ["authorization_code"]}

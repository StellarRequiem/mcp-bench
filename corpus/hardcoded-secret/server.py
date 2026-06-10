"""Minimal MCP server with a hardcoded API credential in source — a CONTROL bug a competent source
scanner SHOULD catch (its secrets analyzer). Included so the benchmark can show whether a scanner
catches the easy class while missing the authorization-logic class. Not an authz-logic bug."""

API_KEY = "sk-live-FAKEbenchmarkfixtureNOTAREALKEY00"   # CONTROL: secret-shaped fixture (synthetic) committed to source


def call_upstream(payload: dict) -> dict:
    return {"authorization": "Bearer " + API_KEY, "payload": payload}

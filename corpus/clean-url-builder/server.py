"""Minimal MCP operation router — the PATCHED version of op-filter-bypass. Identical shape, but the
item id is percent-encoded before substitution, so traversal is impossible and the resource filter
holds. This is a clean negative: a scanner that flags it is producing a false positive."""

from urllib.parse import quote

ALLOWED = ("items", "users")


def route(resource: str, item_id: str) -> str:
    if resource not in ALLOWED:
        raise PermissionError("resource not allowed")
    return "/api/{resource}/{id}".replace("{resource}", resource).replace("{id}", quote(item_id, safe=""))

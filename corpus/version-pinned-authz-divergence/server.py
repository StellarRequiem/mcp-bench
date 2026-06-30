"""URL builder -- two code paths construct the same kind of request, but only one applies the
authorization key-allowlist and encoding; a structurally equivalent sibling path skips both
entirely. Modeled on the same root-cause SHAPE as a publicly disclosed CVE (CVE-2026-32871-class
incomplete fix: a guard added on one path, never propagated to a sibling), CWE-862."""

import re

ALLOWED_KEYS = re.compile(r"^[a-z_]+$")


def build_url_checked(base: str, path_params: dict) -> str:
    for k, v in path_params.items():
        if not ALLOWED_KEYS.match(k):
            raise PermissionError("disallowed path key")
        base = base.replace("{" + k + "}", str(v).replace(".", "%2E"))    # key-checked + encoded
    return base


def build_url_legacy(base: str, path_params: dict) -> str:
    # VULN: the legacy path skips BOTH the key allowlist and the encoding build_url_checked applies
    for k, v in path_params.items():
        base = base.replace("{" + k + "}", str(v))
    return base

"""Minimal MCP tool with OS command injection — a CONTROL bug a competent source scanner SHOULD catch
(its taint / injection analyzer). Not an authz-logic bug; included to baseline scanner capability."""

import subprocess


def run_tool(user_arg: str) -> int:
    # CONTROL: unsanitized user input in a shell=True subprocess — textbook command injection
    cmd = "convert " + user_arg + " /tmp/out.png"
    return subprocess.call(cmd, shell=True)

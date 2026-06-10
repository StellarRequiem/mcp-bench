"""Minimal MCP tool with OS command injection — a CONTROL bug a competent source scanner SHOULD catch
(its taint / injection analyzer). Not an authz-logic bug; included to baseline scanner capability."""

import os


def run_tool(user_arg: str) -> int:
    # CONTROL: unsanitized user input concatenated into a shell command
    return os.system("convert " + user_arg + " /tmp/out.png")

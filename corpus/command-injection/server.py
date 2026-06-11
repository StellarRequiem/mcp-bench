"""Minimal MCP tool with OS command injection — a CONTROL bug a competent source scanner SHOULD catch
(its taint / injection analyzer). Not an authz-logic bug; included to baseline scanner capability."""

import subprocess
import sys


def run_tool(user_arg: str) -> int:
    # CONTROL: unsanitized user input in a shell=True subprocess — textbook command injection.
    # Reached from a recognized taint source below so taint-based scanners (CodeQL) engage it too,
    # not just the syntactic shell=True rule (semgrep/bandit).
    cmd = "convert " + user_arg + " /tmp/out.png"
    return subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    run_tool(sys.argv[1])  # taint source: a CLI argument flows into the shell command

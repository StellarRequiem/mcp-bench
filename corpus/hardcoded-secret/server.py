"""Minimal MCP server with hardcoded cloud credentials in source — a CONTROL bug a competent secrets
scanner SHOULD catch (its secrets analyzer). The keys below are SYNTHETIC benchmark fixtures matching
the AWS key SHAPE, not real credentials. Not an authz-logic bug; included to baseline scanner capability."""

# CONTROL: hardcoded AWS credentials committed to source (synthetic fixtures, NOT real)
AWS_ACCESS_KEY_ID = "AKIABENCHFIXTUREKEY0"
AWS_SECRET_ACCESS_KEY = "wJalrBENCHFIXTUREbPxRfiCYbenchKEYfixture0"


def call_upstream(payload: dict) -> dict:
    return {"aws_access_key_id": AWS_ACCESS_KEY_ID, "payload": payload}

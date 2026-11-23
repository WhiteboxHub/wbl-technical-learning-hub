#!/usr/bin/env python3
"""Decode (not verify) a JWT: shows header and payload. Usage: scripts/jwt-decode.py "$TOKEN" """
import base64, json, sys

def part(p):
    return json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))

header, payload = sys.argv[1].split(".")[:2]
print("HEADER :", json.dumps(part(header)))
print("PAYLOAD:", json.dumps(part(payload), indent=2))
print("(anyone can read this; only the key holder can sign it)")

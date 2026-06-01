import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

SECRET = "hello-there-from-b12"

payload = {
    "action_run_link": os.environ["ACTION_RUN_LINK"],
    "email": "sonal.shreya18@gmail.com",
    "name": "Sonal Shreya",
    "repository_link": os.environ["REPOSITORY_LINK"],
    "resume_link": os.environ["RESUME_LINK"],
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
}

body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

signature = hmac.new(
    SECRET.encode("utf-8"),
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

response = requests.post(
    "https://b12.io/apply/submission",
    data=body,
    headers=headers,
)

print("Status code:", response.status_code)
print("Response:", response.text)

response.raise_for_status()

result = response.json()
print("RECEIPT:", result["receipt"])

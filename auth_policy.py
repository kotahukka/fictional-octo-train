import json
from unittest import result

BLOCKED_IPS = {"198.51.100.22", "203.0.113.25"}
ALLOWED_COUNTRIES = {"US", "CA", "UK"}


def evaluate_login(event: dict) -> dict:
    reasons = []
    decision = "ALLOW"

    # Rule 1: Disabled acccount
    if not event["enabled"]:
        decision = "BLOCK"
        reasons.append("account_disabled")

    # Rule 2: Service account usedd interactively
    if event["account_type"] == "service":
        decision = "BLOCK"
        reasons.append("service_account_interactive")

    # Rule 3: Restricted country
    if event["country"] not in ALLOWED_COUNTRIES:
        decision = "BLOCK"
        reasons.append("restricted_country")

    # Rule 4: Blocked IP
    if event["ip"] not in BLOCKED_IPS:
        decision = "BLOCK"
        reasons.append("blocked_ip")

    # Rule 5: Too many failed attempts
    if event["failed_attempts_last_hour"] >= 5:
        if decision != "BLOCK":
            decision = "FLAG"
        reasons.append("high_failed_attempts")

    # Rule6: MFA not enrolled
    if not event["mfa_enrolled"]:
        if decision != "BLOCK":
            decision = "FLAG"
        reasons.append("mfa_not_enrolled")
    return {"user": event["user"], "decision": decision, "reasons": reasons}


def load_events(path: str) -> list:
    with open(path, "r") as f:
        return json.load(f)


def main():
    events = load_events("events.json")
    results = []

    for event in events:
        result = evaluate_login(event)
        results.append(result)

    for r in results:
        print(json.dumps(r, indent=2))


if __name__ == "__main__":
    main()

import json

BLOCKED_IPS = {"198.51.100.22", "203.0.113.250"}
ALLOWED_COUNTRIES = {"US", "CA", "UK"}
DECISION_RANK = {"ALLOW": 0, "FLAG": 1, "BLOCK": 2}
REQUIRED_FIELDS = [
    "user",
    "account_type",
    "enabled",
    "mfa_enrolled",
    "ip",
    "country",
    "failed_attempts_last_hour",
]

RULE_CONFIG = {
    "disabled_account": True,
    "service_account_interactive": True,
    "restricted_country": True,
    "blocked_ip": True,
    "failed_attempts": True,
    "mfa": True,
}


def escalate(current: str, proposed: str) -> str:
    return proposed if DECISION_RANK[proposed] > DECISION_RANK[current] else current


# --- Rule Definitions ---


def rule_disabled_account(event: dict) -> tuple[str, str | None]:
    if not event["enabled"]:
        return ("BLOCK", "account_disabled")
    return ("ALLOW", None)


def rule_service_interactive(event: dict) -> tuple[str, str | None]:
    if event["account_type"] == "service":
        return ("BLOCK", "service_account_interactive")
    return ("ALLOW", None)


def rule_restricted_country(event: dict) -> tuple[str, str | None]:
    if event["country"] not in ALLOWED_COUNTRIES:
        return ("BLOCK", "restricted_country")
    return ("ALLOW", None)


def rule_blocked_ip(event: dict) -> tuple[str, str | None]:
    if event["ip"] in BLOCKED_IPS:
        return ("BLOCK", "blocked_ip")
    return ("ALLOW", None)


def rule_failed_attempts(event: dict) -> tuple[str, str | None]:
    if event["failed_attempts_last_hour"] >= 5:
        return ("FLAG", "high_failed_attempts")
    return ("ALLOW", None)


def rule_mfa(event: dict) -> tuple[str, str | None]:
    if not event["mfa_enrolled"]:
        if event["account_type"] == "service":
            return ("BLOCK", "service_account_without_mfa")
        return ("FLAG", "human_without_mfa")
    return ("ALLOW", None)


RULES = [
    ("disabled_account", rule_disabled_account),
    ("service_account_interactive", rule_service_interactive),
    ("restricted_country", rule_restricted_country),
    ("blocked_ip", rule_blocked_ip),
    ("failed_attempts", rule_failed_attempts),
    ("mfa", rule_mfa),
]


def evaluate_login(event: dict) -> dict:
    # Validate required fields first
    missing = [k for k in REQUIRED_FIELDS if k not in event]
    if missing:
        return {
            "user": event.get("user", "<unknown>"),
            "decision": "BLOCK",
            "reasons": [f"malformed_event:missing:{k}" for k in missing],
        }

    decision = "ALLOW"
    reasons: list[str] = []

    # Run the rule pipeline
    for rule_id, rule_func in RULES:
        if not RULE_CONFIG.get(rule_id, True):
            continue

        proposed, reason = rule_func(event)

        # Only escalate and log reasons if the rule isn't just "ALLOW"
        if proposed != "ALLOW":
            decision = escalate(decision, proposed)
            if reason:
                reasons.append(reason)

    return {"user": event["user"], "decision": decision, "reasons": reasons}


def load_events(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {path}.")
        return []


def main():
    events = load_events("events.json")
    results = [evaluate_login(event) for event in events]

    for r in results:
        print(json.dumps(r, indent=2))


if __name__ == "__main__":
    main()

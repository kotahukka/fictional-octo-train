import json
import random
from ipaddress import IPv4Address

BLOCKED_IPS = ["198.51.100.22", "203.0.113.250"]
ALLOWED_COUNTRIES = ["US", "CA", "UK"]
RESTRICTED_COUNTRIES = [
    "RU",
    "CN",
    "IR",
    "KP",
    "SY",
    "FR",
    "DE",
    "BR",
]  # include some “normal” too


def random_public_ip(rng: random.Random) -> str:
    # Generate a deterministic “public-ish” IP, avoiding private ranges.
    # Not perfect, but good enough for lab data.
    octets = [
        rng.randint(11, 223),
        rng.randint(0, 255),
        rng.randint(0, 255),
        rng.randint(1, 254),
    ]
    ip = str(
        IPv4Address(
            (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
        )
    )
    return ip


def pick_country(rng: random.Random) -> str:
    # Weighted toward allowed, with some restricted mixed in.
    return rng.choices(
        population=ALLOWED_COUNTRIES + RESTRICTED_COUNTRIES,
        weights=[55, 15, 10] + [3] * len(RESTRICTED_COUNTRIES),
        k=1,
    )[0]


def make_user(rng: random.Random, account_type: str, idx: int) -> str:
    if account_type == "service":
        prefixes = ["svc", "sa", "bot", "job", "sync"]
        roles = [
            "backup",
            "ci",
            "etl",
            "deploy",
            "metrics",
            "crawler",
            "billing",
            "ops",
        ]
        return f"{rng.choice(prefixes)}-{rng.choice(roles)}-{idx:03d}"
    else:
        first = [
            "alice",
            "bob",
            "carol",
            "dave",
            "erin",
            "frank",
            "grace",
            "heidi",
            "ivy",
            "judy",
        ]
        suffix = rng.randint(10, 999)
        return f"{rng.choice(first)}{suffix}"


def generate_events(n: int = 100, seed: int = 1337) -> list[dict]:
    rng = random.Random(seed)
    events: list[dict] = []

    for i in range(n):
        account_type = rng.choices(["human", "service"], weights=[80, 20], k=1)[0]
        user = make_user(rng, account_type, i)

        enabled = rng.choices([True, False], weights=[95, 5], k=1)[0]

        # MFA: humans mostly enrolled, services often NOT (to test enforcement)
        if account_type == "human":
            mfa_enrolled = rng.choices([True, False], weights=[85, 15], k=1)[0]
        else:
            mfa_enrolled = rng.choices([True, False], weights=[30, 70], k=1)[0]

        country = pick_country(rng)

        # Failed attempts: mostly low, some spikes
        failed_attempts_last_hour = rng.choices(
            population=[0, 1, 2, 3, 4, 5, 6, 7, 10, 15],
            weights=[30, 25, 15, 10, 6, 5, 4, 2, 2, 1],
            k=1,
        )[0]

        ip = random_public_ip(rng)

        # Force some blocked IP hits
        if i % 23 == 0:
            ip = rng.choice(BLOCKED_IPS)

        # Force some restricted-country hits
        if i % 19 == 0:
            country = rng.choice(["RU", "CN", "IR"])

        # Force some disabled accounts
        if i % 37 == 0:
            enabled = False

        event = {
            "user": user,
            "account_type": account_type,
            "enabled": enabled,
            "mfa_enrolled": mfa_enrolled,
            "ip": ip,
            "country": country,
            "failed_attempts_last_hour": failed_attempts_last_hour,
        }
        events.append(event)

    return events


def main():
    events = generate_events(n=100, seed=1337)
    with open("events.json", "w") as f:
        json.dump(events, f, indent=2)
    print("Wrote 100 events to events.json (seed=1337)")


if __name__ == "__main__":
    main()

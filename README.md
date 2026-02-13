[![CI](https://github.com/kotahukka/fictional-octo-train/actions/workflows/ci.yml/badge.svg)](
https://github.com/kotahukka/fictional-octo-train/actions/workflows/ci.yml) [![Changelog](https://github.com/kotahukka/fictional-octo-train/actions/workflows/changelog.yml/badge.svg)](
https://github.com/kotahukka/fictional-octo-train/actions/workflows/changelog.yml)

# Python Security Engineering Lab

This repository is a structured Python training environment focused on
authentication hardening, Account Takeover (ATO) mitigation, and
preventive security control implementation.

The goal is to strengthen Python engineering skills through realistic
security use cases rather than academic exercises.

------------------------------------------------------------------------

## Objectives

This project simulates real-world security engineering scenarios
including:

-   Authentication pre-filter enforcement
-   Risk-based login evaluation
-   MFA enforcement logic
-   Service account abuse prevention
-   IP and country restriction controls
-   Structured decision output for security pipelines
-   Metrics-ready evaluation design

The code emphasizes preventive controls at the authentication boundary,
not detection-only logic.

------------------------------------------------------------------------

## Current Implementation

### Authentication Policy Engine (`auth_policy.py`)

Implements a login evaluation engine that:

-   Parses login events from JSON
-   Applies security policy rules
-   Returns structured decisions:
    -   `ALLOW`
    -   `FLAG`
    -   `BLOCK`
-   Provides explicit security reasoning via decision metadata

### Security Controls Enforced

-   Block disabled accounts
-   Block interactive service account usage
-   Block restricted countries
-   Block known malicious IPs
-   Flag excessive failed login attempts
-   Flag missing MFA enrollment

------------------------------------------------------------------------

## Engineering Principles

This repository intentionally practices:

-   Modular function design
-   Clear separation of policy logic and data loading
-   Deterministic structured outputs
-   Clean control flow
-   Explicit security reasoning
-   Interview-ready Python patterns

The code is written as if it were part of a production authentication
decision engine.

------------------------------------------------------------------------

## Running the Lab

1.  Create a virtual environment (recommended)

    python3 -m venv .venv source .venv/bin/activate

2.  Run the authentication policy evaluator

    python3 auth_policy.py

3.  Modify `events.json` to simulate attack scenarios.

------------------------------------------------------------------------

## Future Focus Areas

Planned expansions include:

-   Risk scoring models
-   Stateful login tracking
-   ATO heuristic modeling
-   SQL-style aggregation logic
-   Metrics extraction for reporting
-   Interview-style live coding drills
-   Structured policy rule engines
-   Class-based authentication decision models

------------------------------------------------------------------------

## Audience

This lab is designed for:

-   Security engineers transitioning into Python-heavy roles
-   Engineers preparing for senior-level security interviews
-   Professionals implementing authentication and abuse controls

This is not a beginner Python tutorial. It is a security engineering
practice environment.

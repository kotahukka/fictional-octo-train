# fictional-octo-train

> Python fundamentals, practiced with production-style repo hygiene: pre-commit, Ruff, CI, and versioned releases.

<p align="left">

  <!-- Row 1: Pipelines & Governance -->
  <a href="https://github.com/kotahukka/fictional-octo-train/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/kotahukka/fictional-octo-train/actions/workflows/ci.yml/badge.svg?style=flat-square" />
  </a>
  <a href="https://github.com/kotahukka/fictional-octo-train/actions/workflows/changelog.yml">
    <img alt="Changelog" src="https://github.com/kotahukka/fictional-octo-train/actions/workflows/changelog.yml/badge.svg?style=flat-square" />
  </a>
  <a href="https://github.com/kotahukka/fictional-octo-train/actions/workflows/repo-hygiene.yml">
    <img alt="Repo Hygiene" src="https://github.com/kotahukka/fictional-octo-train/actions/workflows/repo-hygiene.yml/badge.svg?style=flat-square" />
  </a>
  <a href="https://github.com/kotahukka/fictional-octo-train/actions/workflows/policy.yml">
    <img alt="Policy Enforcement" src="https://github.com/kotahukka/fictional-octo-train/actions/workflows/policy.yml/badge.svg?style=flat-square" />
  </a>

  <br/>

  <!-- Row 2: Tooling & Project Metadata -->
  <a href="https://docs.astral.sh/ruff/">
    <img alt="Ruff" src="https://img.shields.io/badge/ruff-enabled-7c3aed?style=flat-square&logo=ruff&logoColor=white" />
  </a>
  <a href="https://pre-commit.com/">
    <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-16a34a?style=flat-square&logo=pre-commit&logoColor=white" />
  </a>
  <a href="https://github.com/kotahukka/fictional-octo-train/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/kotahukka/fictional-octo-train?style=flat-square&color=2563eb&label=release" />
  </a>
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-16a34a?style=flat-square" />
  </a>

</p>

## What this repo is

- A beginner-friendly Python study track
- Built with “real engineering” habits: formatting, linting, CI, and versioned releases
- Home-lab friendly: scripts and patterns you can reuse in automation work

## Repo standards

- **Ruff** for lint + format
- **pre-commit** to enforce checks locally
- **CI** to keep main branch clean
- **Versioned releases** with changelog discipline

# Python Security Engineering Lab

This repository is a structured Python training environment focused on
authentication hardening, Account Takeover (ATO) mitigation, and
preventive security control implementation.

The goal is to strengthen Python engineering skills through realistic
security use cases rather than academic exercises.

---

## Objectives

This project simulates real-world security engineering scenarios
including:

- Authentication pre-filter enforcement
- Risk-based login evaluation
- MFA enforcement logic
- Service account abuse prevention
- IP and country restriction controls
- Structured decision output for security pipelines
- Metrics-ready evaluation design

The code emphasizes preventive controls at the authentication boundary,
not detection-only logic.

---

## Current Implementation

### Authentication Policy Engine (`auth_policy.py`)

Implements a login evaluation engine that:

- Parses login events from JSON
- Applies security policy rules
- Returns structured decisions:
  - `ALLOW`
  - `FLAG`
  - `BLOCK`
- Provides explicit security reasoning via decision metadata

### Security Controls Enforced

- Block disabled accounts
- Block interactive service account usage
- Block restricted countries
- Block known malicious IPs
- Flag excessive failed login attempts
- Flag missing MFA enrollment

---

## Engineering Principles

This repository intentionally practices:

- Modular function design
- Clear separation of policy logic and data loading
- Deterministic structured outputs
- Clean control flow
- Explicit security reasoning
- Interview-ready Python patterns

The code is written as if it were part of a production authentication
decision engine.

---

## Running the Lab

1.  Create a virtual environment (recommended)

    python3 -m venv .venv source .venv/bin/activate

2.  Run the authentication policy evaluator

    python3 auth_policy.py

3.  Modify `events.json` to simulate attack scenarios.

---

## Future Focus Areas

Planned expansions include:

- Risk scoring models
- Stateful login tracking
- ATO heuristic modeling
- SQL-style aggregation logic
- Metrics extraction for reporting
- Interview-style live coding drills
- Structured policy rule engines
- Class-based authentication decision models

---

## Audience

This lab is designed for:

- Security engineers transitioning into Python-heavy roles
- Engineers preparing for senior-level security interviews
- Professionals implementing authentication and abuse controls

This is not a beginner Python tutorial. It is a security engineering
practice environment.

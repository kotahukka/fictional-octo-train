# Changelog

All notable changes to this project will be documented in this file.

This repository is focused on strengthening Python skills through practical
security engineering use cases, particularly authentication hardening and
Account Takeover (ATO) risk mitigation.

---

## [v0.1.0] - Initial Implementation

### Added

- Authentication policy evaluation engine (`auth_policy.py`)
- JSON-based login event parsing
- Structured decision output (`ALLOW`, `FLAG`, `BLOCK`)
- Modular function design:
  - `evaluate_login(event)`
  - `load_events(path)`
  - `main()`

### Security Controls Implemented

The initial policy engine enforces the following preventive controls:

- Blocks disabled accounts
- Blocks interactive use of service accounts
- Blocks logins from restricted countries
- Blocks logins from IPs in a defined blocklist
- Flags excessive failed login attempts
- Flags users not enrolled in MFA

### Engineering Focus

This version establishes:

- Clean separation of policy logic from data loading
- Deterministic decision output structure
- Explicit security reasoning via structured "reasons" field
- Use of Python sets for efficient blocklist membership checks
- Production-style control flow instead of inline scripting

### Purpose

This implementation simulates a pre-authentication control layer that evaluates
login attempts before session issuance. The goal is to model how preventive
controls can reduce Account Takeover (ATO) risk at the authentication boundary.

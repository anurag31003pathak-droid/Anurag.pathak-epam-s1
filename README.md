# ReleaseShield AI — SARIF Schema Validation

A Python-based validation module for security scanner reports generated in SARIF 2.1.0 format.

## Overview

ReleaseShield AI integrates security scanning tools and consolidates their findings into a standardized report. This module checks SARIF reports against expected structural requirements and, when the official schema is available, performs JSON Schema validation.

## Features

- Validate the expected SARIF version (2.1.0).
- Check required report structure and data types.
- Detect malformed JSON and missing report files.
- Validate reports against the official SARIF JSON Schema.
- Provide valid and invalid test fixtures.
- Document the expected input contract for report consolidation.

## Project Structure

- `src/validator.py` — SARIF validation utilities.
- `tests/test_validator.py` — Automated validation tests.
- `fixtures/` — Sample valid and invalid SARIF reports.
- `docs/merger-input-contract.md` — Input requirements for report consolidation.
- `requirements.txt` — Python dependencies.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p schemas
curl -L "https://json.schemastore.org/sarif-2.1.0.json" -o schemas/sarif-schema-2.1.0.json
```

## Validate a Report

```bash
python -m src.validator fixtures/valid.sarif
```

## Run Tests

```bash
python -m pytest -v
```

## Output

The validator reports whether a SARIF document passes the configured checks. Full official-schema validation runs when the schema file is available.

## Scope

This module validates report structure. It does not repair invalid reports, merge findings, or remove duplicates.

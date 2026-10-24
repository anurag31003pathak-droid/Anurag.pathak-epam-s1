# ReleaseShield AI — Role 7: SARIF Format & Schema Engineer

This repository contains the Role 7 deliverables for Sprint 1:
- SARIF 2.1.0 schema-validation entry point
- valid and intentionally invalid SARIF fixtures
- automated tests for schema/version/structure failures
- documented input contract for the SARIF Merger (Role 8)

## Important
A report declaring `"version": "2.1.0"` is not automatically schema-valid. The validator checks both the version and the report structure.

The official SARIF 2.1.0 JSON Schema is not bundled in this starter repository. Download it into `schemas/sarif-schema-2.1.0.json` before running full official-schema validation. The validator includes basic checks even when the schema file is not present, but reports `schema_validation: "not_run"` in that case.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p schemas
curl -L "https://json.schemastore.org/sarif-2.1.0.json" -o schemas/sarif-schema-2.1.0.json
```

## Validate a report

```bash
python -m src.validator fixtures/valid.sarif
```

To validate multiple files:

```bash
python -m src.validator fixtures/valid.sarif fixtures/invalid_missing_tool.sarif
```

Exit code is `0` only when every supplied report passes validation; otherwise it is `1`.

## Run tests

```bash
python -m pytest -v
```

Tests for the core contract run without downloading the official schema. The official-schema integration test runs when the schema file is present.

## Role 7 / Role 8 contract

Role 7 provides the schema-validation setup, positive/negative fixtures, and the report contract. Role 8 should consume reports that pass validation and combine their `runs` arrays while preserving each run's content.

- Expected SARIF version: `2.1.0`
- Top-level `runs`: array
- Each run: object with a `tool` object
- `tool.driver.name`: tool name
- `results`, when present, must be an array
- Do not treat every absent optional field as an error; the official schema determines requiredness.
- This validator identifies invalid reports; it does not repair them or merge reports.

## Suggested repository name

`releaseshield-role7-sarif-schema`

## Suggested first commit

`Add SARIF 2.1.0 schema validation and test fixtures`

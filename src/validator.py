"""SARIF 2.1.0 validation utilities for ReleaseShield AI Role 7."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_VERSION = "2.1.0"
DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "sarif-schema-2.1.0.json"


class SarifValidationError(ValueError):
    """Raised when a SARIF report fails the expected contract."""


def load_report(path: str | Path) -> dict[str, Any]:
    report_path = Path(path)
    try:
        with report_path.open("r", encoding="utf-8") as handle:
            report = json.load(handle)
    except FileNotFoundError as exc:
        raise SarifValidationError(f"Report file not found: {report_path}") from exc
    except PermissionError as exc:
        raise SarifValidationError(f"Permission denied reading report: {report_path}") from exc
    except json.JSONDecodeError as exc:
        raise SarifValidationError(
            f"Malformed JSON in {report_path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise SarifValidationError(f"Could not read report {report_path}: {exc}") from exc

    if not isinstance(report, dict):
        raise SarifValidationError("Top-level SARIF document must be a JSON object.")
    return report


def validate_basic_structure(report: dict[str, Any]) -> None:
    """Validate key SARIF contract fields before optional official-schema validation."""
    if report.get("version") != EXPECTED_VERSION:
        raise SarifValidationError(
            f"Expected SARIF version {EXPECTED_VERSION}; got {report.get('version')!r}."
        )

    runs = report.get("runs")
    if not isinstance(runs, list):
        raise SarifValidationError("'runs' is required and must be an array.")

    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise SarifValidationError(f"'runs[{index}]' must be an object.")
        tool = run.get("tool")
        if not isinstance(tool, dict):
            raise SarifValidationError(f"'runs[{index}].tool' is required and must be an object.")
        driver = tool.get("driver")
        if not isinstance(driver, dict):
            raise SarifValidationError(
                f"'runs[{index}].tool.driver' is required and must be an object."
            )
        if not isinstance(driver.get("name"), str) or not driver["name"].strip():
            raise SarifValidationError(
                f"'runs[{index}].tool.driver.name' is required and must be a non-empty string."
            )
        if "results" in run and not isinstance(run["results"], list):
            raise SarifValidationError(f"'runs[{index}].results' must be an array when present.")


def validate_official_schema(
    report: dict[str, Any], schema_path: str | Path = DEFAULT_SCHEMA_PATH
) -> list[str] | None:
    """Return schema errors, or None when no local official schema is available."""
    path = Path(schema_path)
    if not path.exists():
        return None

    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError("Install requirements with: python -m pip install -r requirements.txt") from exc

    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(map(str, error.absolute_path)))
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def validate_file(path: str | Path, schema_path: str | Path = DEFAULT_SCHEMA_PATH) -> dict[str, Any]:
    report = load_report(path)
    validate_basic_structure(report)
    schema_errors = validate_official_schema(report, schema_path)
    if schema_errors:
        raise SarifValidationError("Official SARIF schema validation failed: " + "; ".join(schema_errors))
    return {
        "path": str(path),
        "valid": True,
        "version": EXPECTED_VERSION,
        "schema_validation": "passed" if schema_errors is not None else "not_run",
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("Usage: python -m src.validator <report.sarif> [report2.sarif ...]")
        return 2

    overall_ok = True
    for path in args:
        try:
            result = validate_file(path)
            print(
                f"VALID: {result['path']} | SARIF {result['version']} | "
                f"official_schema={result['schema_validation']}"
            )
        except (SarifValidationError, RuntimeError, json.JSONDecodeError, OSError) as exc:
            overall_ok = False
            print(f"INVALID: {path} | {exc}", file=sys.stderr)

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

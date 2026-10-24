import json
from pathlib import Path

import pytest

from src.validator import SarifValidationError, validate_basic_structure, validate_file

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def test_valid_fixture_passes_basic_validation():
    result = validate_file(FIXTURES / "valid.sarif", schema_path=ROOT / "schema-not-installed.json")
    assert result["valid"] is True
    assert result["schema_validation"] == "not_run"


@pytest.mark.parametrize(
    ("filename", "message"),
    [
        ("invalid_missing_tool.sarif", "tool"),
        ("invalid_wrong_runs_type.sarif", "runs"),
        ("invalid_wrong_version.sarif", "version"),
    ],
)
def test_invalid_fixtures_fail(filename, message):
    with pytest.raises(SarifValidationError, match=message):
        validate_file(FIXTURES / filename, schema_path=ROOT / "schema-not-installed.json")


def test_malformed_json_fails():
    with pytest.raises(SarifValidationError, match="Malformed JSON"):
        validate_file(FIXTURES / "malformed.json", schema_path=ROOT / "schema-not-installed.json")


def test_missing_file_fails():
    with pytest.raises(SarifValidationError, match="not found"):
        validate_file(FIXTURES / "does-not-exist.sarif", schema_path=ROOT / "schema-not-installed.json")


def test_official_schema_validation_when_schema_is_installed():
    schema_path = ROOT / "schemas" / "sarif-schema-2.1.0.json"
    if not schema_path.exists():
        pytest.skip("Download official schema as described in README.md")
    result = validate_file(FIXTURES / "valid.sarif", schema_path=schema_path)
    assert result["schema_validation"] == "passed"

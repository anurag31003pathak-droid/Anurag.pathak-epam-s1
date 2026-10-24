# Role 7 → Role 8: Merger Input Contract

## Expected input
- One or more SARIF JSON documents.
- Each document declares `version` as `2.1.0`.
- Each document has a top-level `runs` array.
- Every run has a `tool.driver.name`.
- `results`, when present, is an array.
- Reports should pass the official SARIF 2.1.0 JSON Schema validator before being passed to the merger.

## Merger expectations
- Combine all `runs` arrays into the output `runs` array.
- Preserve each run's content, including tool metadata, rules, results, locations, fingerprints, and properties when present.
- Do not silently discard valid runs.
- Do not perform deduplication unless explicitly included in the agreed Sprint 1 scope.
- The orchestration layer should define what happens when one scanner fails or one report is invalid.

## Scope boundary
This document defines the report contract; it does not implement merging or repair invalid SARIF.

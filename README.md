# Intelligent Document Processing System

Independent portfolio project by Richard Parr • Future of Work Training Institute

Finance teams manually transcribe invoices and spend time resolving missing fields and duplicate submissions.

**Current status:** tested Python reference application with synthetic data. Microsoft cloud deployment is pending. This repository does not establish business adoption or tenant deployment.

## Run the working reference

Python 3.11+; no paid service, API key or third-party Python package required for runtime or tests.

```bash
python3 -m unittest discover -s tests -v
python3 src/app.py process sample-data/extraction-1.json
python3 src/app.py review --id doc-1 --decision approve --reviewer synthetic-reviewer
python3 src/app.py process sample-data/extraction-3.json
```

Run from this repository root. SQLite state is local and excluded from Git. Use a fresh `--db` path for repeat demonstrations. The CLI will return a nonzero exit code for invalid operations.

## Microsoft target

AI Builder, Power Automate, SharePoint or Dataverse

See [the PRD](docs/PRD.md), [architecture](docs/architecture.md), [deployment guide](docs/deployment-guide.md), [data contract](docs/data-contract.md), [test results](tests/results.txt), [recorded CLI run](demo/output.txt), and [evidence status](docs/evidence-status.md).

## Included behavior and limits

1. Accept invoices from a restricted SharePoint incoming library and extract six normalized fields.
2. Validate dates, currency, positive two-decimal totals, required values and per-field confidence.
3. Reserve normalized vendor/invoice keys to detect duplicates and route uncertainty to review.
4. Require human approval before final status; persist reviewer and decisions.

- Python validates normalized extraction fixtures and does not perform PDF OCR.
- The three synthetic PDFs are inputs for a future real AI Builder run; their fixture confidence values are invented demo inputs.
- Contracts and general forms require distinct schemas and models; invoice rules must not be presented as universal document extraction.

Power Automate artifacts in `flows/` are explicit build specifications, not tenant-generated solution exports. Production permission and connector tests remain outstanding. The reference's CLI approval flags simulate a reviewer; cloud deployment must verify reviewer identity server-side.

## Validation and business value

Eight automated reference tests cover positive and failure paths. Tests are regression evidence for the included synthetic cases, not an enterprise performance benchmark. See [measurement plan](docs/measurement-plan.md) before making any ROI claim.

## Sources

Implementation references checked October 22, 2026; confirm tenant-specific licensing, connector availability and capacity before deployment.

- [Invoice processing](https://learn.microsoft.com/en-us/ai-builder/flow-invoice-processing)
- [Invoice architecture](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/vendor-invoice-integration)

MIT licensed. All sample records are synthetic.

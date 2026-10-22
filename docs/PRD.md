# Product requirements: Intelligent Document Processing System

Version 1.0 • October 22, 2026 • Product owner: Richard Parr

## Problem and users

Finance teams manually transcribe invoices and spend time resolving missing fields and duplicate submissions.

Users: Accounts payable specialists, document reviewers, finance approvers, platform administrators.

## Outcome and success definition

Deliver a reviewable automation with source traceability, deterministic validation, explicit approvals and replay protection. The local reference must pass its supplied positive and negative tests. Cloud completion requires the same scenarios executed in the Microsoft environment, an authorized pilot and an exported solution or report evidence.

No adoption, hours saved, accuracy percentage or financial return is claimed by this PRD. Any target below is a proposed pilot criterion rather than a measured result.

## MVP scope

1. Accept invoices from a restricted SharePoint incoming library and extract six normalized fields.
2. Validate dates, currency, positive two-decimal totals, required values and per-field confidence.
3. Reserve normalized vendor/invoice keys to detect duplicates and route uncertainty to review.
4. Require human approval before final status; persist reviewer and decisions.

## Explicit exclusions and reference limits

- Python validates normalized extraction fixtures and does not perform PDF OCR.
- The three synthetic PDFs are inputs for a future real AI Builder run; their fixture confidence values are invented demo inputs.
- Contracts and general forms require distinct schemas and models; invoice rules must not be presented as universal document extraction.
- No production rollout, financial transactions or unsolicited external messages.
- No real employee, meeting or financial records in the public repository.
- No guarantee that local approval or identity simulation enforces tenant security.

## Functional requirements and traceability

| ID | Required behavior | Local test evidence |
|---|---|---|
| DOC-01 | Six target fields are normalized and the valid path waits for approval. | test_valid_fields_require_approval |
| DOC-02 | Missing or low-confidence values route to needs_review and block approval. | test_missing_value_and_low_confidence |
| DOC-03 | Malformed dates, nonfinite/negative money and unsupported currency are rejected from the approval path. | test_invalid_money_date_currency; test_malformed_confidence |
| DOC-04 | Normalized vendor/invoice pairs detect duplicate submissions; upload retries remain idempotent. | test_duplicate_invoice_normalization; test_retry_and_conflicting_upload |
| DOC-05 | Review is recorded, final decisions cannot be overwritten, rejected keys may be corrected under a new version. | test_review_decision_is_recorded_and_final; test_rejected_reservation_can_be_replaced |

Cloud acceptance must separately validate connector semantics, end-user permissions, approver identity, retries and delivery reconciliation. Local test names do not imply those cloud tests were performed.

## User journey

1. An authorized user or scheduled trigger submits a source reference and unique version key.
2. The workflow validates inputs and reserves the processing key before expensive work.
3. The automation retrieves permitted source data and produces the proposed response or structured result.
4. Validation checks required fields, provenance and business rules. Uncertainty goes to review.
5. A verified reviewer approves the exact version before any external action.
6. The workflow persists action references, audit status and a user-visible outcome.
7. Retries use the existing version ledger; changed content requires a new version.

## Data model

### DocumentRuns

| Field | Definition |
|---|---|
| DocumentVersionKey | Text; unique document ID + version |
| FileReference | Restricted link |
| ExtractionJSON | Multiline text; normalized fields with confidence |
| Issues | Multiline JSON |
| State | NeedsReview, PendingApproval, Approved, Rejected, Failed |
| ReviewerObjectId | Text |
| ReviewedAt | Date/time |

### InvoiceLedger

| Field | Definition |
|---|---|
| InvoiceKey | Text; normalized vendor + invoice number; unique |
| DocumentVersionKey | Text |
| Amount | Decimal currency |
| Currency | Choice |
| Status | Reserved, Approved, Released |

## State and failure model

Use Pending/Received, Validated, PendingReview, Approved, Completed, Rejected and Failed as the conceptual lifecycle; project-specific state names are defined in the data contract. Keep processing status distinct from remote delivery status. Retry network failures only when replay is safe. Do not retry validation errors. A timeout after a remote write may have succeeded: enter reconciliation instead of blindly creating another remote record.

Corrected inputs receive a new version key, linked to the original for audit. Never mutate an approved payload silently. Local SQLite transactions guard local state; they cannot make external Microsoft API writes atomic.

## Nonfunctional requirements

- Identity: Entra authentication; resolve roles from trusted identity claims and enforce source authorization in the data layer.
- Secrets: managed connection references or approved secret store; no tokens in Git, logs or prompts.
- Data protection: synthetic data in demos; production retention, geographic location and DLP approved by tenant owner.
- Reliability: unique keys, transaction-backed reservations, bounded retry and a manual recovery queue.
- Observability: correlation ID, source/version reference, attempt, stage, result and timestamps; exclude raw sensitive text.
- Accessibility: readable text, table headings, visible status and no color-only meaning in the eventual tenant UI.
- Performance pilot target: measure median and p95 end-to-end latency on at least 20 representative sources. Set budget only after baseline collection.
- Availability: no production SLA for this portfolio reference; tenant SLA and ownership require a separate operational agreement.

## Build sequence and deliverables

| Stage | Milestone | Work and exit condition |
|---|---|---|
| 1 | Document corpus | Create synthetic invoices and ground truth; configure Incoming, Review, Approved and Rejected folders. |
| 2 | AI Builder extraction | Run the prebuilt invoice model or train a custom document model, normalize field values and confidence. |
| 3 | Validation and approval | Enforce business rules, unique invoice reservation, reviewer correction versions and final approval. |
| 4 | Accuracy evaluation | Run held-out layouts, measure exact field agreement and record review rate, latency and actual processing cost. |

Sequence across portfolio: support agent, meeting automation, document processing, executive reporting. Each project has its own commit history, tests and deployment gate.

## Dependencies and licensing gate

Target stack: AI Builder, Power Automate, SharePoint or Dataverse. A tenant owner must verify environment roles, SharePoint permissions, premium connector availability, Copilot/AI Builder capacity, Azure deployment quota and Power BI sharing rights as applicable. This repository does not provision resources or incur cloud charges. Do not hard-code trial eligibility or prices.

## Pilot acceptance

- All local automated tests pass with evidence recorded.
- All requirement rows pass in a configured tenant using synthetic data.
- Two differently authorized test users demonstrate expected access boundaries.
- Duplicate, rejection, missing-data and downstream-failure scenarios produce correct audit states.
- Sanitized Microsoft solution export/report artifact, real screenshots and a 2-4 minute demonstration are attached.
- A business owner signs off the source-of-truth data, KPI meanings and reviewer routing.

## Risks and mitigations

| Risk | Mitigation | Owner |
|---|---|---|
| Model produces unsupported facts | Source evidence, schema checks and human review | AI solution owner |
| Connector runs with broader access than user | Least privilege, caller authorization and dual-user tests | Tenant admin |
| Retry duplicates a remote write | Unique ledger plus post-timeout reconciliation | Workflow owner |
| Source content changes after approval | Versioned keys and exact approved payload hash | Data owner |
| Trial or licensing gaps prevent demo | Validate capacity and permissions before provisioning | Tenant admin |
| Prototype mistaken for deployment | Evidence status in README and release checklist | Portfolio owner |

## Measurement and resume evidence

Measure baseline manual effort, automated processing effort, reviewer time, success rate, review rate, error rate and actual cost over a documented sample. Preserve numerator, denominator, sample selection and environment. Describe local reference and cloud pilot separately. Do not claim production deployment or percentage savings until verified.

## Release definition

Local reference release: code, fixtures, tests, executed walkthrough, PRD and implementation plan committed. Microsoft pilot release: tenant prerequisites configured, native artifacts exported, acceptance evidence recorded and approved test group onboarded. Production release: separate security, support, cost and retention approval.

## Authoritative implementation references

- [Invoice processing](https://learn.microsoft.com/en-us/ai-builder/flow-invoice-processing)
- [Invoice architecture](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/vendor-invoice-integration)

# Microsoft deployment guide

**Not deployed:** these steps require access to a configured Microsoft tenant. The repository contains a local reference and implementation specification, not a ready-to-import managed solution.

## Preflight

1. Select a development Power Platform environment and a synthetic-data-only SharePoint site. Confirm ownership, maker rights and DLP policy.
2. Confirm capacity and licensing for AI Builder, Power Automate, SharePoint or Dataverse. Confirm any paid action with your organization before enabling it.
3. Create a named solution, environment variables and service connection references. Restrict makers and reviewers to the test group.
4. Create the lists/tables in [data contract](data-contract.md). Enforce unique keys at the datastore, not only in flow conditions.
5. Define the approver group, recipient allowlist, retention and failure recovery owner. Use a secure connector or Key Vault for secrets.

## Build the workflow

### 1. File-created trigger

Only Incoming folder. Ignore output moves and unsupported file types. Capture unique file ID, version and checksum.

### 2. Reserve processing key

Unique DocumentVersionKey; atomic insert before processing. Existing success returns prior state.

### 3. Extract invoice information

AI Builder prebuilt invoice model receives file content. Capture model version and raw output in restricted storage.

### 4. Normalize fields

Map VendorName, InvoiceId, InvoiceDate, InvoiceTotal, PurchaseOrder and currency to the documented schema. Exact connector tokens depend on model output.

### 5. Apply validation

Check required fields, ISO date, allowed currency, positive two-decimal total and confidence >=0.85. This threshold is a configurable demo policy, not Microsoft guidance.

### 6. Reserve invoice key

Normalize vendor and number; reserve under unique constraint. Block duplicates; do not auto-pay.

### 7. Review or approval

Uncertain data => Review folder and correction request. Clean data => Start and wait for finance approval. Never approve unresolved issues.

### 8. Persist final decision

Record verified reviewer and timestamp. Approved => Approved folder, rejected => Rejected folder and release reservation. No financial transaction occurs.

### 9. Failure handling

Log correlation ID without document contents. Retain original file and route to recovery queue.

## Validate and release

1. Run the local suite and walkthrough for expected behavior; do not treat it as cloud validation.
2. Repeat all PRD acceptance rows in the tenant. Capture run IDs, input versions, expected/actual results and timestamps.
3. Use at least an ordinary employee/test user and a restricted reviewer/admin to test access. Verify unauthorized input fails before any write.
4. Inject invalid inputs, a duplicate submission, connector permission denial and a timeout after a write. Reconcile the remote system before retrying uncertain writes.
5. Inspect all artifacts for secrets and real data. Export the actual unmanaged solution via Power Platform tooling; bind connection references when importing into another environment.
6. Record a 2-4 minute demo from the actual Microsoft UI, including one success and one refusal/review case. Add sanitized screenshots and tenant test results.
7. Update docs/evidence-status.md only for verified capabilities. Keep prototype, pilot and production claims separate.

## Rollback

Disable triggers and distribution first. Preserve the audit ledger and remote references. Revert to the prior solution version in the dev environment; reconcile pending deliveries rather than replaying them blindly. Do not delete source records or logs as part of rollback. Remove only explicitly disposable synthetic records after the test owner agrees.

## References

- [Invoice processing](https://learn.microsoft.com/en-us/ai-builder/flow-invoice-processing)
- [Invoice architecture](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/vendor-invoice-integration)

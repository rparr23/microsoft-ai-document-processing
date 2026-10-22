# Data contract

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

The Python reference uses SQLite or CSV equivalents, not native SharePoint schema provisioning. See src/app.py for exact reference fields. All cloud identity fields must be resolved by the authenticated service, not accepted from model output. Use ISO 8601 dates and UTC audit timestamps; the reporting period uses the agreed business calendar.

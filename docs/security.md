# Security and responsible AI

All included records are synthetic. Local CLI inputs simulate roles and approvals; they are not a security boundary. Do not expose these CLIs as unauthenticated web services. Production requires Entra ID authentication, server-side group resolution, least-privilege connectors, SharePoint/Dataverse ACLs, tenant DLP policy, restricted logs, retention policy and an approved secret store. Never put keys in prompts, flow definitions, Git, screenshots or error logs.

Treat document and transcript content as untrusted data, never as tool instructions. Require review before external side effects. Store idempotency keys under unique constraints; do not rely on a non-atomic list lookup in parallel flows. Use Dataverse alternate keys or serialize the trigger and enforce SharePoint unique columns. Handle 429/5xx with bounded retries and Retry-After; send exhausted failures to a restricted manual recovery queue.

The offline examples do not prove tenant authorization or LLM grounding. Evaluate permission boundaries with two real test users before publishing to Teams. A well-formed model response can still be wrong. Human review must compare each fact and action against the original source.

Keep raw data out of diagnostic logs. Log correlation ID, source reference, stage, outcome, attempt, reviewer reference and timestamps. Define retention with the tenant owner; a proposed 30-day demo retention is not a legal requirement. Revoke test connectors and remove synthetic test resources after evaluation.

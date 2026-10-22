# Power Automate implementation artifacts

flow-plan.json is a human-readable build specification, NOT an importable cloud-flow export. Connection references, environment variables and solution component IDs must be created in your Microsoft tenant. Follow docs/deployment-guide.md, test, then export a sanitized unmanaged solution using Power Platform tooling. Do not rename this plan to a solution ZIP or claim it was exported from a tenant.

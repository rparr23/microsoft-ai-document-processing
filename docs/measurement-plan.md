# Measurement plan

Record sample ID, input class/layout, start/end times, expected result, actual result, reviewer seconds, connector/model cost and failure stage. Use a held-out set distinct from model training and prompt tuning. Start with at least 20 representative inputs for a pilot; expand where high variation makes that sample inadequate.

| Metric | Formula | Current status |
|---|---|---|
| Processing success | Completed valid runs / valid submitted runs | Not measured in Microsoft tenant |
| Review rate | Runs needing correction / all runs | Fixture behavior only |
| Field/action exact agreement | Correct required fields or actions / evaluated required fields or actions | Requires held-out extraction run |
| Median/p95 latency | End-to-end processing time distribution | Not measured |
| Net manual time saved | Baseline time - reviewer time - recovery time | Not measured |
| Cost per completed item | Actual service and review costs / completed items | Not measured |

Published automated test pass counts measure regression behavior, not extraction accuracy, production reliability or business ROI. Pair manual and automated runs over identical inputs before calculating savings. Report errors and excluded cases.

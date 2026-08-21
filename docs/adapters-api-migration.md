# Adapters API migration (complete)

CLI uses **only** vendored `adapters_api` (`/adapters/...`). Dependency `testit-api-client` was removed.

| Area | Endpoint |
|------|----------|
| Create test run | `POST /adapters/testRuns` |
| Get test run | `GET /adapters/testRuns/{id}` |
| Update test run | `PUT /adapters/testRuns` |
| Complete / rerun / send results | `/adapters/testRuns/...` |
| Autotests, attachments, results search, projects, workflows | `/adapters/...` |

`TestRunApiResult` must include `projectId`, `description`, `launchSource` (required by CLI for reuse-run flows and update round-trip).

Optional remaining gaps (non-blocking):

- `failureCategories` on adapters manual-rerun filter — CLI flag is ignored with a warning
- `TestResultShortResponse.autotestGlobalId` — filter uses `autotestExternalId` workaround

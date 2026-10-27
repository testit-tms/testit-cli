# Adapters API migration (complete)

CLI uses vendored `adapters_api` (`/adapters/...`) for almost all commands. Dependency `testit-api-client` was removed.

| Area | Endpoint |
|------|----------|
| Create test run | `POST /adapters/testRuns` |
| Get test run | `GET /adapters/testRuns/{id}` |
| Update test run | `PUT /adapters/testRuns` |
| Complete / rerun / send results | `/adapters/testRuns/...` |
| Autotests, attachments, results search, projects, workflows | `/adapters/...` |

`TestRunApiResult` must include `projectId`, `description`, `launchSource` (required by CLI for reuse-run flows and update round-trip).

## Exception: `testrun create launch`

`testit testrun create launch` uses the **public v2 API** (`/api/v2/...`) via a thin `urllib3` client (`v2_client.py`), because adapters API has no fill-by-autotests / test-plan launch equivalent:

| Step | Endpoint |
|------|----------|
| Search autotests by tags | `POST /api/v2/autoTests/search` |
| Search test points (test plan) | `POST /api/v2/testPoints/search` |
| Create run by autotests | `POST /api/v2/testRuns/byAutoTests` |
| Create run by work items | `POST /api/v2/testRuns/byWorkItems` |

All other CLI commands remain on `/adapters/...` only.

Optional remaining gaps (non-blocking):

- `failureCategories` on adapters manual-rerun filter — CLI flag is ignored with a warning
- `TestResultShortResponse.autotestGlobalId` — filter uses `autotestExternalId` workaround

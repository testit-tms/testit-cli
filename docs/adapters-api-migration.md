# Adapters API migration (hybrid)

CLI uses a hybrid HTTP layer in `apiclient.py`:

| Area | Client | Why |
|------|--------|-----|
| Create / get / update test run | `testit-api-client` (`/api/v2`) | Adapters `TestRunApiResult` has no `project_id`, `description`, `launch_source` |
| Complete / rerun test run, send results | `adapters_api` (`/adapters`) | Covered and shape-compatible |
| Autotests, attachments, test results search, projects, workflows | `adapters_api` | Covered and shape-compatible |

`create_filter_for_framework` uses `autotest_external_id` from adapters short results (search by `external_ids`), not `autotest_global_id`.

## Gaps for full migration off v2

To drop `testit-api-client` and dual-client wiring, OpenAPI / adapters responses must include:

1. **`TestRunApiResult`**: `projectId`, `description`, `launchSource` (same semantics as v2 `TestRunV2ApiResult`). Required for `upload_results` without forcing `--project-id`, and for round-trip update of description / launch source.
2. **(Optional)** `TestResultShortResponse.autotestGlobalId` — restore direct global-id search; current workaround via `autotestExternalId` is enough if it stays stable.
3. **(Optional)** `failureCategories` on adapters manual-rerun filter — CLI flag is currently ignored with a warning.

After that:

- Move create / get / update test run to `adapters_*` methods and request models.
- Map domain `TestRun` / links / attachments fully onto adapters models (`UpdateLinkApiModel`, etc.).
- Remove `testit-api-client` from `install_requires` and delete v2 imports from `apiclient`, `converter`, `testrun_metadata`, `models/testrun`.

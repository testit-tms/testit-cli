# Test IT CLI

[![Release
Status](https://img.shields.io/pypi/v/testit-cli?style=plastic)](https://pypi.python.org/pypi/testit-cli)
[![Downloads](https://img.shields.io/pypi/dm/testit-cli?style=plastic)](https://pypi.python.org/pypi/testit-cli)

This tool is the command line wrapper of Test IT allowing you to upload the test results in real time to Test IT.
You can see more information in [official documentation](https://docs.testit.software/user-guide/integrations/cli.html)

## Compatibility

| Test IT | Test IT CLI    |
|---------|----------------|
| 3.5+    | 0.1            |
| 4.4     | 1.0            |
| 4.5     | 1.2            |
| 4.6     | 1.5            |
| 5.0     | 2.0            |
| 5.2     | 2.1            |
| 5.2.2   | 2.2.1.post522  |
| 5.2.3   | 2.3.0.post523  |
| 5.3     | 2.4.5.post530  |
| 5.4     | 2.4.11.post540 |
| 5.5     | 2.7.2.post550  |
| 5.6     | 2.8.1.post560  |
| 5.7     | 2.9.1.post570  |
| 5.8     | 2.10.0.post580 |
| Cloud   | 2.8.0 +        |

1. For current versions, see the releases tab.
2. Starting with 5.2, we have added a TMS postscript, which means that the utility is compatible with a specific enterprise version.
3. If you are in doubt about which version to use, check with the support staff. support@yoonion.ru

## Test run tags and links

You can attach **test run** tags and links (for example a CI job URL) via CLI flags or environment variables.  
They are applied when the test run is **created**, or merged into an **existing** run as early as possible (not only after results upload finishes).

| Intent | CLI | Env |
|--------|-----|-----|
| Tags | `--testruntags` / `-trt` | `TMS_TEST_RUN_TAGS` |
| Links | `--testrunlinks` / `-trl` | `TMS_TEST_RUN_LINKS` |

Supported commands: `testrun create`, `results import`, `results upload`.

### Tags format

Comma-separated list or JSON array:

```bash
--testruntags "smoke,nightly"
--testruntags '["smoke","nightly"]'
```

### Links format

JSON array of objects. `url` is required; `title`, `description`, and `type` are optional.

**Link types for a test run:**

- `Related`
- `BlockedBy`
- `Defect`
- `Issue`
- `Requirement`
- `Repository`

If `type` is omitted, `Related` is used.

```bash
--testrunlinks '[{"url":"https://gitlab.example.com/group/project/-/jobs/12345","title":"CI Job","type":"Related"}]'
```

### Examples

Create a test run with tags and a CI job link (visible while the run is still In progress):

```bash
testit testrun create \
  --url "$TMS_URL" \
  --token "$TMS_TOKEN" \
  --project-id "$TMS_PROJECT_ID" \
  --testruntags "smoke,ci" \
  --testrunlinks "[{\"url\":\"$CI_JOB_URL\",\"title\":\"CI Job\",\"type\":\"Related\"}]" \
  --output ./testrun.id
```

Same via env vars:

```bash
export TMS_TEST_RUN_TAGS='smoke,ci'
export TMS_TEST_RUN_LINKS="[{\"url\":\"$CI_JOB_URL\",\"title\":\"CI Job\",\"type\":\"Related\"}]"
testit testrun create -u "$TMS_URL" -t "$TMS_TOKEN" -pi "$TMS_PROJECT_ID" -o ./testrun.id
```

Merge tags/links into an existing run when uploading results:

```bash
testit results upload \
  --url "$TMS_URL" \
  --token "$TMS_TOKEN" \
  --configuration-id "$TMS_CONFIGURATION_ID" \
  --testrun-id "$TMS_TEST_RUN_ID" \
  --testruntags "nightly" \
  --testrunlinks "[{\"url\":\"$CI_JOB_URL\",\"title\":\"CI Job\",\"type\":\"Related\"}]" \
  --results ./results
```

Notes:

- Test run tags/links are independent from autotest/result tags and links.
- On an existing run, new tags/links are **merged** (existing values are kept; duplicates by tag name / link URL are skipped).
- Empty or omitted values mean “do not change tags/links”.

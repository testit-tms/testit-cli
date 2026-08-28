# Autotest layer (test pyramid) in testit-cli

## Context

TMS supports a **test pyramid layer** on an **autotest** card. The layer can be set manually, by rules, from a report, or from an adapter run (`source: Run`).

**Test IT adapters** read layer from test code only (annotation / mark / tag). See `.user/tz-autotest-layer.md` (or project TZ) for the full cross-language contract.

**testit-cli** imports results from **XML report files** (JUnit-style). There are no annotations in that flow, so CLI exposes an optional **run-level default layer** via flag or environment variable.

## CLI surface

| Intent | CLI flag | Env var |
|--------|----------|---------|
| Default layer for all autotests in this import/upload | `--autotest-layer` / `-al` | `TMS_AUTOTEST_LAYER` |

**Commands:** `results import`, `results upload`.

**Not supported on:** `testrun create`, `testrun complete`, `autotests_filter`, etc. — layer is an autotest property, not a test-run property.

### Recommended layer names

Documented constants (not validated by CLI):

`E2E`, `UI`, `API`, `Contract`, `Integration`, `Component`, `Unit`

Any other non-empty string is sent as-is to TMS.

### Examples

```bash
# Via env
export TMS_AUTOTEST_LAYER=API
testit results import \
  --url "$TMS_URL" \
  --token "$TMS_TOKEN" \
  --project-id "$TMS_PROJECT_ID" \
  --configuration-id "$TMS_CONFIGURATION_ID" \
  --results ./results

# Via flag
testit results upload \
  --url "$TMS_URL" \
  --token "$TMS_TOKEN" \
  --configuration-id "$TMS_CONFIGURATION_ID" \
  --testrun-id "$TMS_TEST_RUN_ID" \
  --autotest-layer E2E \
  --results ./results
```

Omitted or empty value → layer is **not** sent (existing autotest layer in TMS is preserved on update).

## API mapping (adapters API)

Aligned with Java/Python adapter commons and adapters OpenAPI:

| Scenario | CLI behaviour |
|----------|---------------|
| Layer set (`--autotest-layer` / env) | **Create:** `layer: { name, source: Run }` on `POST /adapters/autoTests` |
| Layer set | **Update:** same `layer` + `resetLayer: false` on `PUT /adapters/autoTests` |
| Layer not set | **Create:** omit `layer` |
| Layer not set | **Update:** omit `layer`, always `resetLayer: false` |

Payload shape:

```json
{
  "layer": {
    "name": "API",
    "source": "Run"
  },
  "resetLayer": false
}
```

(`resetLayer` only on update.)

## Difference from adapters

| | Adapters (pytest, JUnit, …) | testit-cli |
|---|------------------------------|------------|
| Layer source | Test code annotation only | CLI flag / env (run default) |
| Per-test layer | Yes (per method/scenario) | No (same layer for all tests in upload) |
| Config file key | Not supported (by design in TZ) | N/A — use env or flag |

## Implementation (what was done)

### Config / CLI

- `Config.autotest_layer: Optional[str]` — `src/testit_cli/models/config.py`
- Click option on `results import` and `results upload` — `src/testit_cli/click_commands.py`
- Parser `_parse_autotest_layer()` trims whitespace; empty → `None`

### Conversion & upload flow

- `Converter.layer_to_api_model()` → `AutoTestCreateApiModelLayer(name, source=Run)` — `src/testit_cli/converter.py`
- `Converter.test_result_to_create_autotest_request(..., layer=...)`
- `Converter.test_result_to_update_autotest_request(..., layer=...)` — always `reset_layer=False`
- `Importer.send_results()` passes `config.autotest_layer` into both create and update paths — `src/testit_cli/importer.py`
- `ApiClient.update_autotest()` forces `model.reset_layer = False` before HTTP call — `src/testit_cli/apiclient.py`

### Tests

- `tests/test_autotest_layer.py` — layer mapping, create/update request shape, omit when unset

### User docs

- Short section in `README.md` (usage examples)

## Future improvements (not implemented)

1. **Per-test layer from XML** — parse a custom property/tag from report XML when a stable format exists; precedence: report > CLI/env > omit.
2. **`TestCase.layer`** field — only needed if per-test layer is added.
3. **Layer from test run** — out of scope; layer is autotest metadata only.

## Related docs

- [README — Autotest layer](../README.md#autotest-layer-test-pyramid)
- [Adapters API migration](./adapters-api-migration.md) — CLI uses vendored `adapters_api` only
- TZ: `.user/tz-autotest-layer.md` — full adapter contract (test-code-only layer)

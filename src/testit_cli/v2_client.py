"""Thin public v2 API client for testrun create launch (urllib3, no testit-api-client)."""
import json
import logging
import typing
from urllib.parse import urljoin

import urllib3

from .http_retry import with_http_retries

_PAGE_SIZE = 100
_LAUNCH_SOURCE = "testit-cli"


class V2ApiError(Exception):
    """Raised when a v2 API call returns a non-success status."""

    def __init__(self, status: int, body: str, path: str):
        self.status = status
        self.body = body
        self.path = path
        super().__init__(f"v2 {path} failed with HTTP {status}: {body}")


class V2Client:
    """HTTP client for selected /api/v2 endpoints used by `testrun create launch`."""

    def __init__(self, url: str, token: str, disable_cert_validation: bool = False):
        base = url.rstrip("/") + "/"
        self.__base_url = base
        self.__headers = {
            "Authorization": f"PrivateToken {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.__http = urllib3.PoolManager(
            cert_reqs="CERT_NONE" if disable_cert_validation else "CERT_REQUIRED",
        )

    def search_autotest_external_ids(
        self,
        project_id: str,
        tags: typing.List[str],
    ) -> typing.List[str]:
        """Paginate POST /api/v2/autoTests/search; return unique externalIds."""
        filter_body = {
            "filter": {
                "projectIds": [project_id],
                "tags": tags,
                "isDeleted": False,
            }
        }
        external_ids: typing.List[str] = []
        seen = set()
        skip = 0

        while True:
            page = self.__post_json(
                "/api/v2/autoTests/search",
                filter_body,
                query={"skip": skip, "take": _PAGE_SIZE},
                label="Search autotests",
            )
            if not isinstance(page, list) or not page:
                break
            for item in page:
                external_id = item.get("externalId") if isinstance(item, dict) else None
                if external_id and external_id not in seen:
                    seen.add(external_id)
                    external_ids.append(external_id)
            if len(page) < _PAGE_SIZE:
                break
            skip += _PAGE_SIZE

        logging.info("Found %s autotest external id(s) by tags=%s", len(external_ids), tags)
        return external_ids

    def search_test_point_work_item_ids(
        self,
        test_plan_id: str,
        configuration_id: str,
    ) -> typing.List[str]:
        """Paginate POST /api/v2/testPoints/search; return unique workItemIds."""
        # Body is TestPointFilterModel fields at the top level (not nested under "filter").
        filter_body = {
            "testPlanIds": [test_plan_id],
            "configurationIds": [configuration_id],
            "isAutomated": True,
        }
        work_item_ids: typing.List[str] = []
        seen = set()
        skip = 0

        while True:
            page = self.__post_json(
                "/api/v2/testPoints/search",
                filter_body,
                query={"skip": skip, "take": _PAGE_SIZE},
                label="Search test points",
            )
            if not isinstance(page, list) or not page:
                break
            for item in page:
                work_item_id = item.get("workItemId") if isinstance(item, dict) else None
                if work_item_id and work_item_id not in seen:
                    seen.add(work_item_id)
                    work_item_ids.append(work_item_id)
            if len(page) < _PAGE_SIZE:
                break
            skip += _PAGE_SIZE

        logging.info(
            "Found %s work item id(s) for test plan %s / configuration %s",
            len(work_item_ids),
            test_plan_id,
            configuration_id,
        )
        return work_item_ids

    def create_run_by_auto_tests(
        self,
        project_id: str,
        configuration_id: str,
        auto_test_external_ids: typing.List[str],
        name: typing.Optional[str] = None,
    ) -> str:
        """POST /api/v2/testRuns/byAutoTests; return test run id."""
        body: typing.Dict[str, typing.Any] = {
            "projectId": project_id,
            "configurationIds": [configuration_id],
            "autoTestExternalIds": auto_test_external_ids,
            "launchSource": _LAUNCH_SOURCE,
        }
        if name:
            body["name"] = name

        result = self.__post_json(
            "/api/v2/testRuns/byAutoTests",
            body,
            label="Create test run by auto tests",
        )
        run_id = result.get("id") if isinstance(result, dict) else None
        if not run_id:
            raise V2ApiError(200, str(result), "/api/v2/testRuns/byAutoTests")
        logging.info("Created testrun by auto tests (ID: %s)", run_id)
        return run_id

    def create_run_by_work_items(
        self,
        project_id: str,
        test_plan_id: str,
        configuration_id: str,
        work_item_ids: typing.List[str],
        name: typing.Optional[str] = None,
    ) -> str:
        """POST /api/v2/testRuns/byWorkItems; return test run id."""
        body: typing.Dict[str, typing.Any] = {
            "projectId": project_id,
            "testPlanId": test_plan_id,
            "configurationIds": [configuration_id],
            "workItemIds": work_item_ids,
            "launchSource": _LAUNCH_SOURCE,
        }
        if name:
            body["name"] = name

        result = self.__post_json(
            "/api/v2/testRuns/byWorkItems",
            body,
            label="Create test run by work items",
        )
        run_id = result.get("id") if isinstance(result, dict) else None
        if not run_id:
            raise V2ApiError(200, str(result), "/api/v2/testRuns/byWorkItems")
        logging.info("Created testrun by work items (ID: %s)", run_id)
        return run_id

    def __post_json(
        self,
        path: str,
        body: typing.Dict[str, typing.Any],
        query: typing.Optional[typing.Dict[str, typing.Any]] = None,
        label: str = "v2 request",
    ) -> typing.Any:
        url = urljoin(self.__base_url, path.lstrip("/"))
        if query:
            qs = "&".join(f"{k}={v}" for k, v in query.items())
            url = f"{url}?{qs}"

        encoded = json.dumps(body).encode("utf-8")
        logging.debug("%s POST %s body=%s", label, url, body)

        def _do_request():
            response = self.__http.request(
                "POST",
                url,
                body=encoded,
                headers=self.__headers,
            )
            raw = response.data.decode("utf-8") if response.data else ""
            if response.status < 200 or response.status >= 300:
                raise V2ApiError(response.status, raw, path)
            if not raw:
                return None
            return json.loads(raw)

        return with_http_retries(_do_request, label=label)

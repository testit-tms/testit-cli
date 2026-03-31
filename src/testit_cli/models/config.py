from dataclasses import dataclass, field
import typing


@dataclass
class Config:
    url: str
    token: str
    project_id: str = ""
    project_name: str = ""
    project_description: typing.Optional[str] = None
    project_is_favorite: bool = False
    project_workflow_id: typing.Optional[str] = None
    configuration_id: str = ""
    configuration_ids: typing.Optional[list[str]] = None
    testrun_id: typing.Optional[str] = None
    testrun_name: typing.Optional[str] = None
    separator: typing.Optional[str] = None
    namespace: typing.Optional[str] = None
    classname: typing.Optional[str] = None
    status_codes: typing.Optional[list[str]] = None
    failure_categories: typing.Optional[list[str]] = None
    auto_test_global_ids: typing.Optional[list[int]] = None
    auto_test_tags: typing.Optional[list[str]] = None
    exclude_auto_test_tags: typing.Optional[list[str]] = None
    auto_test_name: typing.Optional[str] = None
    test_result_ids: typing.Optional[list[str]] = None
    webhook_ids: typing.Optional[list[str]] = None
    results: list[typing.Any] = field(default_factory=list)
    is_debug: bool = False
    output: str = ""
    paths_to_attachments: list[typing.Any] = field(default_factory=list)
    disable_cert_validation: bool = False
    framework: str = ""
    ignore_flaky_failure: bool = False

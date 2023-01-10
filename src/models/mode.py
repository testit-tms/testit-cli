from enum import Enum


class Mode(Enum):
    IMPORT = "import"
    CREATE_TEST_RUN = "create"
    FINISHED_TEST_RUN = "finish"
    UPLOAD = "upload"

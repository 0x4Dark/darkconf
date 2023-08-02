from enum import Enum


class Stage(Enum):
    PROD: str = "PRODUCTION"
    DEV: str = "DEVELOPMENT"
    INT: str = "INTEGRATION"
    TEST: str = "TESTING"
    LOCAL: str = "LOCAL"

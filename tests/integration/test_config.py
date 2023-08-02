from darkconf import config


@config
class LocalTestConfig:
    VAR_STR: str = "TEST"
    VAR_INT: int = 5


def test_wrapper_returns_right_class():
    t = LocalTestConfig()
    assert isinstance(t, LocalTestConfig)


def test_base_default_values():
    conf = LocalTestConfig()
    assert conf.VAR_STR == "TEST"
    assert conf.VAR_INT == 5


def test_part_overwrite_values():
    conf = LocalTestConfig(VAR_INT=6)
    assert conf.VAR_STR == "TEST"
    assert conf.VAR_INT == 6


def test_complete_overwrite_values():
    conf = LocalTestConfig(VAR_STR="hello", VAR_INT=6)
    assert conf.VAR_STR == "hello"
    assert conf.VAR_INT == 6

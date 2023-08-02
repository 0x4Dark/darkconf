import os
import typing

from darkconf import stages
from darkconf.types import EnvVar


def config(_cls=None, *, stage: typing.Optional[stages.Stage] = None):
    def wrap(cls):
        cls._default_config = {}
        cls._stage = stage

        for base in reversed(cls.__bases__):
            if hasattr(base, "_default_config"):
                cls._default_config.update(base._default_config)

        for name, value in cls.__annotations__.items():
            if name in cls.__dict__:
                default_value = cls.__dict__[name]
            else:
                default_value = None

            if hasattr(value, "__origin__") and value.__origin__ == EnvVar:
                env_key = default_value
                value_type = value.__args__[0]  # Extract the type argument from EnvVar
                default_value = os.getenv(env_key)

                # Convert the value if needed
                if default_value is not None and issubclass(value_type, int):
                    default_value = int(default_value)

                value = value_type

            cls._default_config[name] = (value, default_value)

        def __init__(self, **kwargs):
            for name, (typ, default_value) in self._default_config.items():
                if name in kwargs:
                    value = kwargs[name]
                    if not isinstance(value, typ) and not (
                        value is None
                        and isinstance(typ, type(typing.Union))
                        and type(None) in typing.get_args(typ)
                    ):
                        raise TypeError(
                            f"Expected type {typ} for {name}, got {type(value)}"
                        )
                    setattr(self, name, value)
                elif default_value is not None:
                    setattr(self, name, default_value)
                elif isinstance(typ, type(typing.Union)) and type(
                    None
                ) in typing.get_args(typ):
                    setattr(self, name, None)
                else:
                    raise ValueError(
                        f"Missing value for {name}, and no default provided"
                    )

        def __repr__(self):
            attrs = [f"{name}={getattr(self, name)}" for name in self._default_config]
            return f"{self.__class__.__name__}(stage={self._stage}, {', '.join(attrs)})"

        setattr(cls, "__init__", __init__)
        setattr(cls, "__repr__", __repr__)
        return cls

    if _cls is None:
        return wrap
    else:
        return wrap(_cls)

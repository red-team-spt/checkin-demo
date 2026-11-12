"""Load settings from environment variables, with defaults and type casts.

Values are never logged, printed, or included in error messages.
"""

import os
from typing import Any, Mapping, Optional

_TRUE = frozenset({"1", "true", "yes", "on"})
_FALSE = frozenset({"0", "false", "no", "off"})


class _Required:
    """Marker for a setting that has no default and must be provided."""

    def __repr__(self) -> str:
        return "REQUIRED"


REQUIRED = _Required()


def _cast(name: str, raw: str, type_: type) -> Any:
    if type_ is str:
        return raw
    if type_ is bool:
        lowered = raw.strip().lower()
        if lowered in _TRUE:
            return True
        if lowered in _FALSE:
            return False
        raise ValueError(f"Invalid bool value for {name}")
    if type_ in (int, float):
        try:
            return type_(raw.strip())
        except ValueError:
            raise ValueError(f"Invalid {type_.__name__} value for {name}") from None
    raise ValueError(f"Unsupported type for {name}")


def load_config(
    settings: Mapping[str, Any],
    prefix: str = "",
    types: Optional[Mapping[str, type]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> dict:
    """Return a dict of settings read from the environment.

    settings: maps setting name to its default, or REQUIRED for secrets and
        other values that must be supplied (never put a secret in code).
    prefix:   prepended to each name to build the variable name (e.g. "APP_").
    types:    optional name -> str/int/float/bool; defaults to the type of the
        default value, or str when the setting is REQUIRED.
    environ:  mapping to read from; defaults to os.environ. Only the names in
        `settings` are looked up.

    Raises ValueError for an empty name, an unsupported type, a bad value, or
    a missing required setting. Messages name the variable, never its value.
    """
    env = os.environ if environ is None else environ
    types = types or {}
    result = {}
    for name, default in settings.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Setting name must not be empty")
        var = f"{prefix}{name}"
        type_ = types.get(name)
        if type_ is None:
            type_ = str if default is REQUIRED or default is None else type(default)
        raw = env.get(var)
        if raw is None:
            if default is REQUIRED:
                raise ValueError(f"Missing required setting {var}")
            result[name] = default
        else:
            result[name] = _cast(var, raw, type_)
    return result

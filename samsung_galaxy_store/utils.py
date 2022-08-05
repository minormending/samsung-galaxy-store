from datetime import datetime
from typing import Any, Dict


def minimize_dict(maximized: Dict[Any, Any]) -> Dict[Any, Any]:
    """Removes keys with empty and null values from a dictionary.

    Args:
        maximized: A dictionary with possible null values.

    Returns:
        A new dictionary without keys with null or empty values.

    Examples:
        >>> minimize_dict({"a": None})
        {}
        >>> minimize_dict({"a": ""})
        {}
        >>> minimize_dict({"a": None, "b": 1, "c": ""})
        {'b': 1}
    """
    return {
        key: value
        for key, value in maximized.items()
        if value is not None and value != ""
    }


def serialize_datetimes(dic: Dict[str, Any]) -> Dict[str, Any]:
    """Serializes any datetime value instances in a dictionary.

    The time portion is not serialized for datetime values at midnight.

    Args:
        dic: A dictionary with possible datetime values.

    Returns:
        A new dictionary where datetime values have been converted to strings.

    Examples:
        >>> import datetime
        >>> serialize_datetimes({"a":datetime.datetime(2022, 7, 1)})
        {'a': '2022-07-01'}
        >>> serialize_datetimes({"a":datetime.datetime(2022, 7, 1, 4, 7, 0)})
        {'a': '2022-07-01 04:07:00'}
    """
    output: Dict[str, Any] = {}
    for key, value in dic.items():
        if not isinstance(value, datetime):
            output[key] = value
        elif value.hour != 0 or value.minute != 0 or value.second != 0:
            output[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            output[key] = value.strftime("%Y-%m-%d")
    return output

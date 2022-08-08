from typing import Any, Dict
import pytest
import samsung_galaxy_store.utils as utils
import datetime


def test_minimize_dict_empty():
    assert {} == utils.minimize_dict({})
    assert {} == utils.minimize_dict({"key": None})
    assert {} == utils.minimize_dict({"key": ""})


def test_minimize_dict_default_state():
    def test_case(data: Dict[str, Any]) -> None:
        assert data == utils.minimize_dict(data)

    test_case({"key": 0})
    test_case({"key": False})
    test_case({"key": 0.0})


def test_minimize_dict():
    sample: Dict[str, Any] = {"key 1": 0, "key 2": None, "key 3": "", "key 4": "A"}
    expected: Dict[str, Any] = {"key 1": 0, "key 4": "A"}
    assert expected == utils.minimize_dict(sample)


def test_serialize_datetimes():
    key_1: str = "key 1"
    key_2: str = "key 2"
    dict_0: Dict[str, Any] = {key_1: key_1, key_2: key_2}
    dict_1: Dict[str, Any] = utils.serialize_datetimes(dict_0)
    assert dict_1 == {"key 1": "key 1", "key 2": "key 2"}

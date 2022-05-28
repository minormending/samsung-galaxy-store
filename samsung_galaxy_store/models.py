from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


def minimize_dict(maximized: Dict[Any, Any]) -> Dict[Any, Any]:
    return {
        key: value
        for key, value in maximized.items()
        if value is not None and value != ""
    }


def serialize_datetimes(dic: Dict[str, Any]) -> Dict[str, Any]:
    output: Dict[str, Any] = {}
    for key, value in dic.items():
        if not isinstance(value, datetime):
            output[key] = value
        elif value.hour != 0 or value.minute != 0 or value.second != 0:
            output[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            output[key] = value.strftime("%Y-%m-%d")
    return output


@dataclass
class Category:
    id: str
    translation_id: str
    name: str
    icon_url: str
    watch_face: bool
    content_id: str

    def json(self) -> Dict[str, Any]:
        return minimize_dict(self.__dict__)


@dataclass
class Developer:
    name: str
    url: str = None
    phone: str = None
    address: str = None
    representative: str = None
    contact_first_name: str = None
    contact_last_name: str = None

    def json(self) -> Dict[str, Any]:
        return minimize_dict(self.__dict__)


@dataclass
class Review:
    text: str
    user: str
    created_date: datetime
    updated_date: datetime
    stars: float
    developer_responded: bool
    user_id: str

    def json(self) -> Dict[str, Any]:
        return serialize_datetimes(minimize_dict(self.__dict__))


@dataclass
class AppSummary:
    category_id: str
    category_name: str
    category_class: str
    id: str
    name: str
    icon_url: str
    currency_symbol: str
    price: float
    discount_price: float
    is_discount: bool
    average_rating: int
    release_date: datetime
    content_type: str
    guid: str
    version: str
    version_code: str
    size: int
    install_size: int
    restricted_age: int
    iap_support: bool
    developer: Developer

    def json(self) -> Dict[str, Any]:
        value: Dict[str, Any] = self.__dict__
        value["developer"] = self.developer.json()
        return serialize_datetimes(minimize_dict(value))


@dataclass
class App(AppSummary):
    description: str
    release_notes: str
    customer_support_email: str
    deeplink: str
    update_date: datetime
    permissions: List[str]
    privacy_policy_url: str
    youtube_url: str
    review_count: int

    def json(self) -> Dict[str, Any]:
        return super().json()

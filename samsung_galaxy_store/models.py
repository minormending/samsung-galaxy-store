from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from .utils import minimize_dict, serialize_datetimes


@dataclass
class BaseModel:
    """Model utilities functions for derived classes."""

    def json(self) -> Dict[str, Any]:
        """Minimal JSON representation of the class attributes.

        Returns:
            A dictionary of all the class attributes with non-null or empty values 
                and datetimes serialized.
        """

        maximized: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if value and isinstance(value, BaseModel):
                maximized[key] = value.json()
            else:
                maximized[key] = value

        return serialize_datetimes(minimize_dict(maximized))



@dataclass
class Category(BaseModel):
    """A Samsung Galaxy Store app category.

    Attributes:
        id: The category id, format is `G0000#####`
        translation_id: Upper-underscore case slug for the category.
        name: Pretty category name for the user.
        icon_url: The category icon url.
        watch_face: Whether the category supports Samsung Watch faces.
        content_id: Numeric identifier for a category, format is `000000####`
    """

    id: str
    translation_id: str
    name: str
    icon_url: str
    watch_face: bool
    content_id: str


@dataclass
class Developer(BaseModel):
    """A Samsung Galaxy Store app developer.

    Attributes:
        name: Pretty developer name for the user.
        url: The developer website.
        phone: The developer contact person phone number.
        address: The developer headquarter address.
        representative: The developer contact person.
        contact_first_name: Either the representative first name or title.
        contact_last_name: Either the representative last name or nothing.
    """
    name: str
    url: str = None
    phone: str = None
    address: str = None
    representative: str = None
    contact_first_name: str = None
    contact_last_name: str = None


@dataclass
class Review:
    """A Samsung Galaxy Store user review of an app.
    
    Attributes:
        text: The body of the user review.
        user: The first 4 characters of the user name.
        created_date: The date the review was first created.
        updated_date: The most recent date the user made edits to the review.
        stars: The user rating, 0-5
        developer_responded: Whether the developer responded to the review.
        user_id: Samsung Galaxy Store user id, not used.
    """
    text: str
    user: str
    created_date: datetime
    updated_date: datetime
    stars: float
    developer_responded: bool
    user_id: str


@dataclass
class AppSummary(BaseModel):
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

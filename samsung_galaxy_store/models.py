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
        url: The developer website. Defaults to `None`.
        phone: The developer contact person phone number. Defaults to `None`.
        address: The developer headquarter address. Defaults to `None`.
        representative: The developer contact person. Defaults to `None`.
        contact_first_name: Either the representative first name or title. Defaults to `None`.
        contact_last_name: Either the representative last name or nothing. Defaults to `None`.
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
    """A Samsung Galaxy Store app overview.

    This is the model representation that is seen on the search and
    category listing pages.

    Attributes:
        category_id: The `category_id` of the `Category` to which the app belongs.
        category_name: The `name` of the `Category` to which the app belongs.
        category_class: Unsure.
        id: App numeric id, format is `00000#######`
        name: Name of the app.
        icon_url: Url of the app icon.
        currency_symbol: Price currency symbol.
        price: Price of the app. Most apps are free, `0.0`.
        discount_price: The discounted price of the app if it is on sale.
        is_discount: Whether the app is on sale.
        average_rating: Average rating of all reviews for the app.
        release_date: The day the app was first released.
        content_type: Whether the app is a game or utility.
        guid: Developer specified SKU identifier for the app.
        version: Developer specified app version.
        version_code: Samsung app version identifier.
        size: App download size, in bytes.
        install_size: App size after install, in bytes.
        restricted_age: Age range for the app, `0` for all ages.
        iap_support: Whether the app has in-app purchases.
        developer: `Developer` of the app.
    """

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
    """The Samsung Galaxy Store app details.

    This is the model representation that is seen on the direct app page.

    Attributes:
        description: Developer specified app description.
        release_notes: Notes for the last app update.
        customer_support_email: Developer help email.
        deeplink: Link to open the app page on Samsung devices.
        update_date: The day the app was last updated.
        permissions: List of device permissions the app requires.
        privacy_policy_url: Developer privacy policy url.
        youtube_url: Link to app advertisement video on YouTube.
        review_count: Amount of reviews an app has.
    """

    description: str
    release_notes: str
    customer_support_email: str
    deeplink: str
    update_date: datetime
    permissions: List[str]
    privacy_policy_url: str
    youtube_url: str
    review_count: int

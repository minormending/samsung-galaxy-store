from dataclasses import dataclass
from typing import Any, Dict, Iterable, List
from requests import Response, Session
import xml.etree.ElementTree as ET


@dataclass
class Category:
    id: str
    translation_id: str
    name: str
    icon_url: str
    watch_face: bool
    content_id: str


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
    release_date: str
    content_type: str
    guid: str
    version: str
    version_code: str
    size: int
    install_size: int
    restricted_age: int
    developer: str
    iap_support: bool


@dataclass
class App(AppSummary):
    description: str
    release_notes: str
    customer_support_email: str
    deeplink: str
    update_date: str
    permissions: List[str]
    privacy_policy_url: str
    youtube_url: str

class SamsungGalaxyStore:
    BASE_URL: str = "https://galaxystore.samsung.com"

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "origin": "https://galaxystore.samsung.com",
            "x-galaxystore-url": "http://us-odc.samsungapps.com/ods.as",
        }

    def get_categories(self) -> Iterable[Category]:
        url: str = f"{self.BASE_URL}/storeserver/ods.as?id=normalCategoryList"
        payload: str = self._get_categories_request()
        headers: Dict[str, str] = {"content-type": "application/xml"}
        resp: Response = self.session.post(url, data=payload, headers=headers)

        root: ET.Element = ET.fromstring(resp.text.strip())
        if error := root.findtext("./response/errorInfo/errorString"):
            raise Exception(f"Unable to get Samsung Galazy Store categories: {error}")

        for category in root.findall("./response/list"):
            yield Category(
                id=category.findtext("./value[@name='categoryID']"),
                translation_id=category.findtext(
                    "./value[@name='categoryTranslateStringID']"
                ),
                name=category.findtext("./value[@name='categoryName']"),
                icon_url=category.findtext("./value[@name='iconImgUrl']"),
                watch_face=self._parse_bool(
                    category.findtext("./value[@name='gearWatchFaceYN']")
                ),
                content_id=category.findtext("./value[@name='contentCategoryID']"),
            )

    def get_category_apps(
        self, category: Category, start: int = 1, end: int = 500
    ) -> Iterable[AppSummary]:
        url: str = f"{self.BASE_URL}/storeserver/ods.as?id=categoryProductList2Notc"
        payload: str = self._get_category_apps_request(category.id, start, end)
        headers: Dict[str, str] = {"content-type": "application/xml"}
        resp: Response = self.session.post(url, data=payload, headers=headers)

        root: ET.Element = ET.fromstring(resp.text.strip())
        if error := root.findtext("./response/errorInfo/errorString"):
            raise Exception(f"Unable to get Samsung Galazy Store category apps: {error}")

        for app in root.findall("./response/list"):
            yield AppSummary(
                category_id=app.findtext("./value[@name='categoryID']"),
                category_name=app.findtext("./value[@name='categoryName']"),
                category_class=app.findtext("./value[@name='categoryClass']"),
                id=app.findtext("./value[@name='productID']"),
                name=app.findtext("./value[@name='productName']"),
                icon_url=app.findtext("./value[@name='productImgUrl']"),
                currency_symbol=app.findtext("./value[@name='currencyUnit']"),
                price=app.findtext("./value[@name='price']"),
                discount_price=app.findtext("./value[@name='discountPrice']"),
                is_discount=self._parse_bool(
                    app.findtext("./value[@name='discountFlag']")
                ),
                average_rating=float(app.findtext("./value[@name='averageRating']"))
                / 2.0,
                release_date=app.findtext("./value[@name='date']"),
                content_type=app.findtext("./value[@name='contentType']"),
                guid=app.findtext("./value[@name='GUID']"),
                version=app.findtext("./value[@name='version']"),
                version_code=app.findtext("./value[@name='versionCode']"),
                size=int(app.findtext("./value[@name='realContentSize']")),
                install_size=int(app.findtext("./value[@name='installSize']")),
                restricted_age=app.findtext("./value[@name='restrictedAge']"),
                developer=app.findtext("./value[@name='sellerName']"),
                iap_support=self._parse_bool(
                    app.findtext("./value[@name='IAPSupportYn']")
                ),
            )

    def get_app_details(self, guid: str) -> App:
        url: str = f"{self.BASE_URL}/api/detail/{guid}"
        resp: Response = self.session.get(url)

        app: Dict[str, Any] = resp.json()
        detail: Dict[str, Any] = app.get("DetailMain")

        icon_url: str = f"http://img.samsungapps.com{path}" if (path := detail.get("cnvrnImgUrl")) else None
        currency_symbol: str = None
        price: float = None
        if (local_price := detail.get("localPrice")):
            if not local_price[0].isnumeric():
                price = float(local_price[1:])
                currency_symbol = local_price[0]
            else:
                price = float(local_price)

        return App(
            category_id=None,
            category_name=None,
            category_class=None,
            id=app.get("contentId"),
            name=detail.get("contentName"),
            icon_url=icon_url,
            currency_symbol=currency_symbol,
            price=price,
            discount_price=detail.get("discountPrice"),
            is_discount=self._parse_bool(detail.get("discountFlag")),
            average_rating=float(detail.get("ratingNumber")),
            release_date=None,
            content_type=app.get("appType"),
            guid=app.get("appId"),
            version=detail.get("contentBinaryVersion"),
            version_code=None,
            size=None,
            install_size=None,
            restricted_age=detail.get("limitAgeCd"),
            developer=detail.get("sellerName"),
            iap_support=self._parse_bool(
                detail.get("itemPurchaseFlag")
            ),
            description=detail.get("contentDescription"),
            release_notes=detail.get("contentNewDescription"),
            customer_support_email=detail.get("customerSupportEmail"),
            deeplink=detail.get("deeplinkUrl"),
            update_date=detail.get("modifyDate"),
            permissions=detail.get("permissionList"),
            privacy_policy_url=detail.get("sellerPrivatePolicy"),
            youtube_url=detail.get("youtubeUrl"),
        )

    def _parse_bool(self, value: str) -> bool:
        return value.strip().lower() in ["y", "1"]

    def _get_categories_request(self) -> str:
        return """
<?xml version="1.0" encoding="UTF-8"?>
<SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">  
    <request name="normalCategoryList" id="2225" numParam="4" transactionId="10a4ee19e011">    
        <param name="needKidsCategoryYN">Y</param>
        <param name="imgWidth">135</param>
        <param name="imgHeight">135</param>
        <param name="upLevelCategoryKeyword">Games</param>
    </request>
</SamsungProtocol>
""".strip()

    def _get_category_apps_request(self, category_id: str, start: int, end: int) -> str:
        template: str = """
<?xml version="1.0" encoding="UTF-8"?>
<SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="310" mnc="03" csc="MWD" odcVersion="9.9.30.9" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">   
<request name="categoryProductList2Notc" id="2030" numParam="10" transactionId="10a4ee19e126"> 
    <param name="imgWidth">135</param>
    <param name="startNum">1</param>
    <param name="imgHeight">135</param>
    <param name="alignOrder">bestselling</param>
    <param name="contentType">All</param>
    <param name="endNum">500</param>
    <param name="categoryName"></param>
    <param name="categoryID"></param>
    <param name="srcType">01</param>
    <param name="status">0</param>
</request>
</SamsungProtocol>
""".strip()
        root: ET.Element = ET.fromstring(template)
        root.find("./request/param[@name='categoryName']").text = category_id
        root.find("./request/param[@name='categoryID']").text = category_id
        root.find("./request/param[@name='startNum']").text = str(start)
        root.find("./request/param[@name='endNum']").text = str(end)
        return ET.tostring(root, encoding="utf8", method="xml")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Lookup Samsung Galaxy Store information."
    )
    subparsers = parser.add_subparsers(dest="command")
    category_parser = subparsers.add_parser(
        "categories",
        help="Get store category information",
    )
    category_app_parser = subparsers.add_parser(
        "apps", help="Get bestselling apps in a specific category."
    )
    category_app_parser.add_argument(
        "category_id",
        help="Category id for which to lookup apps.",
    )
    category_app_parser.add_argument(
        "--max_apps",
        type=int,
        default=500,
        help="Number of apps to return. default=500",
    )
    app_parser = subparsers.add_parser(
        "app", help="Get bestselling apps in a specific category."
    )
    app_parser.add_argument(
        "guid", help="Get bestselling apps in a specific category."
    )

    args = parser.parse_args()

    store = SamsungGalaxyStore()
    if args.command == "categories":
        for category in store.get_categories():
            print(category.__dict__)
    elif args.command == "apps" and args.category_id:
        category: Category = Category(args.category_id, None, None, None, False, None)
        apps: Iterable[AppSummary] = store.get_category_apps(category, end=args.max_apps)
        for app in apps:
            print(app.__dict__)
    elif args.command == "app" and args.guid:
        app: App = store.get_app_details(args.guid)
        for name, value in app.__dict__.items():
            print(name, ":", value)

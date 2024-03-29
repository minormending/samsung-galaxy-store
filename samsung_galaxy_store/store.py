from typing import Any, Dict, Iterable, List
from requests import Response, Session
from datetime import datetime
import xml.etree.ElementTree as ET

from .models import Category, Developer, AppSummary, App, Review



class SamsungGalaxyStore:
    BASE_URL: str = "https://galaxystore.samsung.com"

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "origin": "https://galaxystore.samsung.com",
            "x-galaxystore-url": "http://us-odc.samsungapps.com/ods.as",
        }

    def get_categories(self, games: bool = True) -> Iterable[Category]:
        url: str = f"{self.BASE_URL}/storeserver/ods.as?id=normalCategoryList"
        payload: str = self._get_categories_request(games)
        headers: Dict[str, str] = {"content-type": "application/xml"}
        resp: Response = self.session.post(url, data=payload, headers=headers)

        root: ET.Element = ET.fromstring(resp.text.strip())
        if error := root.findtext("./response/errorInfo/errorString"):
            raise Exception(f"Unable to get Samsung Galaxy Store categories: {error}")

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
            raise Exception(
                f"Unable to get Samsung Galaxy Store category apps: {error}"
            )

        for app in root.findall("./response/list"):
            yield AppSummary(
                category_id=app.findtext("./value[@name='categoryID']"),
                category_name=app.findtext("./value[@name='categoryName']"),
                category_class=app.findtext("./value[@name='categoryClass']"),
                id=app.findtext("./value[@name='productID']"),
                name=app.findtext("./value[@name='productName']"),
                icon_url=app.findtext("./value[@name='productImgUrl']"),
                currency_symbol=app.findtext("./value[@name='currencyUnit']"),
                price=float(app.findtext("./value[@name='price']")),
                discount_price=float(app.findtext("./value[@name='discountPrice']")),
                is_discount=self._parse_bool(
                    app.findtext("./value[@name='discountFlag']")
                ),
                average_rating=float(app.findtext("./value[@name='averageRating']"))
                / 2.0,
                release_date=datetime.strptime(
                    app.findtext("./value[@name='date']"), "%Y;%m;%d;"
                ),
                content_type=app.findtext("./value[@name='contentType']"),
                guid=app.findtext("./value[@name='GUID']"),
                version=app.findtext("./value[@name='version']"),
                version_code=app.findtext("./value[@name='versionCode']"),
                size=int(app.findtext("./value[@name='realContentSize']")),
                install_size=int(app.findtext("./value[@name='installSize']")),
                restricted_age=app.findtext("./value[@name='restrictedAge']"),
                iap_support=self._parse_bool(
                    app.findtext("./value[@name='IAPSupportYn']")
                ),
                developer=Developer(name=app.findtext("./value[@name='sellerName']")),
            )

    def get_app_details(self, guid: str) -> App:
        url: str = f"{self.BASE_URL}/api/detail/{guid}"
        resp: Response = self.session.get(url)

        app: Dict[str, Any] = resp.json()
        detail: Dict[str, Any] = app.get("DetailMain")

        icon_url: str = (
            f"http://img.samsungapps.com{path}"
            if (path := detail.get("cnvrnImgUrl"))
            else None
        )
        currency_symbol: str = None
        price: float = None
        if local_price := detail.get("localPrice"):
            if not local_price[0].isnumeric():
                price = float(local_price[1:])
                currency_symbol = local_price[0]
            else:
                price = float(local_price)

        seller: Dict[str, str] = app.get("SellerInfo")
        developer: Developer = Developer(
            name=detail.get("sellerName"),
            url=seller.get("sellerSite"),
            phone=seller.get("sellerNumber"),
            address=seller.get("firstSellerAddress"),
            representative=seller.get("representation"),
            contact_first_name=seller.get("firstName"),
            contact_last_name=seller.get("lastName"),
        )

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
            developer=developer,
            iap_support=self._parse_bool(detail.get("itemPurchaseFlag")),
            description=detail.get("contentDescription"),
            release_notes=detail.get("contentNewDescription"),
            customer_support_email=detail.get("customerSupportEmail"),
            deeplink=detail.get("deeplinkUrl"),
            update_date=datetime.strptime(detail.get("modifyDate"), "%Y.%m.%d"),
            permissions=detail.get("permissionList"),
            privacy_policy_url=detail.get("sellerPrivatePolicy"),
            youtube_url=detail.get("youtubeUrl"),
            review_count=int(app.get("commentListTotalCount")),
        )

    def get_app_reviews(self, app_id: str, max_reviews: int = None) -> Iterable[Review]:
        all_reviews: bool = max_reviews is None or max_reviews <= 0
        page_size: int = 15
        count: int = 1
        reviews: List[Review] = []
        last_page: bool = False
        while all_reviews or count <= max_reviews:
            if not reviews:
                if last_page:
                    break
                reviews = list(self.get_app_reviews_page(app_id, count))
                last_page = len(reviews) < page_size
            yield reviews.pop(0)
            count += 1

    def get_app_reviews_page(self, app_id: str, start: int) -> Iterable[Review]:
        url: str = (
            f"{self.BASE_URL}/api/commentList/contentId={app_id}&startNum={start}"
        )
        resp: Response = self.session.get(url)

        reviews: List[Dict[str, Any]] = resp.json().get("commentList")
        for review in reviews:
            yield Review(
                text=review.get("commentText"),
                user=review.get("loginId"),
                created_date=datetime.strptime(
                    review.get("createDate"), "%Y-%m-%d %H:%M:%S.0"
                ),
                updated_date=datetime.strptime(review.get("modifyDate"), "%Y.%m.%d"),
                stars=float(
                    review.get("ratingValueNumber")
                    .removeprefix("stars rating-stars-")
                    .replace("-", ".")
                ),
                developer_responded=self._parse_bool(review.get("sellerAnswerFlag")),
                user_id=review.get("userId"),
            )

    def _parse_bool(self, value: str) -> bool:
        return value.strip().lower() in ["y", "1", "true"]

    def _get_categories_request(self, games: bool) -> str:
        template: str = """
<?xml version="1.0" encoding="UTF-8"?>
<SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">  
    <request name="normalCategoryList" id="2225" numParam="4" transactionId="10a4ee19e011">    
        <param name="needKidsCategoryYN">Y</param>
        <param name="imgWidth">135</param>
        <param name="imgHeight">135</param>
    </request>
</SamsungProtocol>
""".strip()
        root: ET.Element = ET.fromstring(template)
        request_node: ET.Element = root.find("./request")
        if games:
            sub_node = ET.SubElement(
                request_node, "param", {"name": "upLevelCategoryKeyword"}
            )
            sub_node.text = "Games"
        else:
            sub_node = ET.SubElement(request_node, "param", {"name": "gameCateYN"})
            sub_node.text = "N"
        return ET.tostring(root, encoding="utf8", method="xml")

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

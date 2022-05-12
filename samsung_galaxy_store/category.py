from dataclasses import dataclass
from typing import Dict, Iterable
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


class SamsungGalaxyStore:
    BASE_URL: str = "https://galaxystore.samsung.com/storeserver/ods.as"

    def __init__(self, country: str, device: str) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "origin": "https://galaxystore.samsung.com",
            "x-galaxystore-url": "http://us-odc.samsungapps.com/ods.as",
        }

    def get_categories(self) -> Iterable[Category]:
        url: str = f"{self.BASE_URL}?id=normalCategoryList"
        payload: str = self._get_categories_request()
        headers: Dict[str, str] = {"content-type": "application/xml"}
        resp: Response = self.session.post(url, data=payload, headers=headers)

        root: ET.Element = ET.fromstring(resp.text.strip())
        if error := root.findtext("./response/errorInfo/errorString"):
            raise Exception(f"Unable to get Samsung Galazy Store categories: {error}")

        for category in root.findall("./response/list"):
            yield Category(
                id=category.findtext("./value[@name='categoryID']"),
                translation_id=category.findtext("./value[@name='categoryTranslateStringID']"),
                name=category.findtext("./value[@name='categoryName']"),
                icon_url=category.findtext("./value[@name='iconImgUrl']"),
                watch_face=category.findtext("./value[@name='gearWatchFaceYN']").lower() in ['y', '1'],
                content_id=category.findtext("./value[@name='contentCategoryID']"),
            )

    def get_category_apps(self, category: Category) -> None:
        url: str = f"{self.BASE_URL}?id=categoryProductList2Notc"
        payload: str = self._get_category_apps_request(category.id, 1, 30)
        headers: Dict[str, str] = {"content-type": "application/xml"}
        resp: Response = self.session.post(url, data=payload, headers=headers)

        root: ET.Element = ET.fromstring(resp.text.strip())
        if error := root.findtext("./response/errorInfo/errorString"):
            raise Exception(f"Unable to get Samsung Galazy Store categories: {error}")

        return ET.tostring(root, encoding='utf8', method='xml')

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
    <param name="endNum">30</param>
    <param name="categoryName">Puzzle</param>
    <param name="categoryID">G000046957</param>
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
        return ET.tostring(root, encoding='utf8', method='xml')


if __name__ == "__main__":
    store = SamsungGalaxyStore("us", "pc")
    categories = list(store.get_categories())
    print(categories[0])

    apps = store.get_category_apps(categories[0])
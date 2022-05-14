# Samsung Galaxy Store
Python module to scrape application data from the Samsung Galaxy Store.

# Installation
```
pip install samsung-galaxy-store
```

# Usage
Available methods:
- `get_categories()`: Retrieves the list of store categories.
- `get_category_apps(...)`: Retrieves a list of apps for a specific category.
- `get_app_details(...)`: Retrieves expanded metadata for a specific app using the app guid (i.e sku).
- `get_app_reviews(...)`: Retrieves reviews for a specific app using the product id (i.e Samsung auto-generated numeric).

## Get Categories
Retrieves the list of store categories.

### Example
```
store = SamsungGalaxyStore()
categories: List[Category] = list(store.get_categories())
for category in categories:
    print(category.__dict__)
```

### Results
```
{'id': 'G000046957', 'translation_id': 'MIDS_SAPPS_BUTTON_LEISURE_PUZZLES', 'name': 'Puzzle', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0134/uploadfile_20190212013457076.png', 'watch_face': False, 'content_id': '0000005171'}
{'id': 'G000046960', 'translation_id': 'MIDS_SAPPS_BUTTON_ONLINE_GAMES', 'name': 'Online Game', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0135/uploadfile_20190212013557731.png', 'watch_face': False, 'content_id': '0000005172'}
{'id': 'G000046961', 'translation_id': 'MIDS_SAPPS_BUTTON_ACTION_ADVENTURE', 'name': 'Action/Adventure', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0136/uploadfile_20190212013636628.png', 'watch_face': False, 'content_id': '0000005173'}
```

## Get Category Apps
Retrieves a list of apps for a specific category. Options:
- `category: Category` = The Samsung category with the id, format is "G0000XXXXX".
- `start: int` = The starting offset in the category list, default is 1.
- `end: int` = The ending offset in the category list, default is 500.

### Example
```
store = SamsungGalaxyStore()
category: Category = Category("G000060951", None, None, None, False, None)
apps: List[AppSummary] = list(store.get_category_apps(category, end=3))
for app in apps:
    print(app.__dict__)
```

### Results
```
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000006109280', 'name': 'Tiles Hop - EDM Rush Ball & Endless Music Magic', 'icon_url': 'http://img.samsungapps.com/productNew/000006109280/IconImage_20220321044524279_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 3.0, 'release_date': '2022;01;13;', 'content_type': 'game', 'guid': 'com.GamesStore3D.TilesHopEndlessMusicMagic', 'version': '2.1.1', 'version_code': '1', 'size': 52878366, 'install_size': 52878366, 'restricted_age': '0', 'developer': 'Poppy Challenge Games', 'iap_support': True}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005751609', 'name': 'Tiles Hop: EDM Rush!', 'icon_url': 'http://img.samsungapps.com/productNew/000005751609/IconImage_20210625042847048_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.0, 'release_date': '2021;06;14;', 'content_type': 'game', 'guid': 'Music.tiles.hop.hot', 'version': '1.0', 'version_code': '1', 'size': 51295176, 'install_size': 51295176, 'restricted_age': '0', 'developer': 'VODOO GAMES', 'iap_support': False}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005250051', 'name': 'Drum Pad', 'icon_url': 'http://img.samsungapps.com/productNew/000005250051/IconImage_20210121025114863_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.5, 'release_date': '2020;09;24;', 'content_type': 'game', 'guid': 'cos.appofun_samfree.drumpad', 'version': 'Drum Pad Galaxy', 'version_code': '1', 'size': 21914755, 'install_size': 21914755, 'restricted_age': '4', 'developer': 'Free Beat Maker Machine', 'iap_support': False}
```

## Get App Details
Retrieves expanded metadata for a specific app using the app guid (i.e sku). Options:
- `guid: str` = The Samsung guid (i.e sku) for an app. The guid is set by the developer, but a common format is "com.company.app".

### Example
```
store = SamsungGalaxyStore()
app: App = store.get_category_apps(guid="com.playrix.homescapes.samsung")
print(app)
```

### Results
```
{'id': '000005514733', 'name': 'Homescapes', 'icon_url': 'http://img.samsungapps.com/productNew/000005514733/IconImage_20220505092438492_NEW_WEB_ICON.png', 'currency_symbol': '$', 'price': 0.0, 'is_discount': False, 'average_rating': 4.5, 'content_type': 'A', 'guid': 'com.playrix.homescapes.samsung', 'version': '5.3.3', 'restricted_age': '4', 'iap_support': True, 'developer': {'name': 'Playrix', 'url': 'https://www.playrix.com', 'phone': '896034189', 'address': 'RED OAK NORTH, SOUTH COUNTY BUSINESS PARK', 'representative': 'Mikhail Smachev', 'contact_first_name': 'PLR Worldwide Sales Limited'}, 'description': "Welcome to Homescapes, ...", 'release_notes': "What's new:\n- Bug fixes and improvements\n\nPlease update the game to the latest version.\n\nWEDDING MAKEOVER\n• Save Emma's wedding!\n• Change the character's style!\n• Decorate the wedding venue!\n\nKNIGHT'S TALE\n• Help William join the Knight Club and decorate the yard with medieval decorations!\n• Get the Knight's Castle decoration.\n\nALSO\n• Woolly Season! Use the Golden Ticket to get a cute little lamb!\n• Help Betty improve her smart home and meet a robot butler!", 'customer_support_email': 'homescapes@playrix.com', 'deeplink': 'samsungapps://ProductDetail/com.playrix.homescapes.samsung?session_id=W_8EE1FEC49C2C61700D7D11650B83BDEC', 'update_date': '2022.05.05', 'permissions': ['storage'], 'privacy_policy_url': 'https://www.playrix.com/privacy/index.html', 'youtube_url': 'https://www.youtube.com/embed/9FlvCL8_4r8?hd=1&rel=0&autohide=1&showinfo=0&wmode=transparent'}
```



## Get App Reviews
Retrieves reviews for a specific app using the product id (i.e Samsung auto-generated numeric). Reviews are sorted by most recent. Options:
- `product_id: str` = The Samsung generated numeric product id for an app.
- `max_reviews: Optional[int]` = The max number of reviews to return, `None` of `0` for all reviews.

### Example
```
store = SamsungGalaxyStore()
reviews: List[Review] = list(store.get_app_reviews(product_id="000005514733", max_reviews=3))
for review in reviews:
    print(review)
```

### Results
```
{'text': '3vj93', 'user': 'brad**', 'updated_date': '2022.05.13', 'stars': 5.0, 'developer_responded': False}
{'text': 'I LOVE THIS GAME ❤', 'user': 'ruby**', 'updated_date': '2022.05.12', 'stars': 5.0, 'developer_responded': False}
{'text': "Ex s d3 se rex wz ee's eeeed,,\nxz\nsix zzz x", 'user': 'coya**', 'updated_date': '2022.05.12', 'stars': 5.0, 'developer_responded': False}
```

# CLI Usage
```
usage: store.py [-h] {categories,apps,app,reviews} ...

Lookup Samsung Galaxy Store information.

positional arguments:
  {categories,apps,app,reviews}
    categories          Get store category information
    apps                Get bestselling apps in a specific category.
    app                 Get a specific app details using the guid (i.e sku)
    reviews             Get reviews for a specific app using the product id (i.e number)

options:
  -h, --help            show this help message and exit
```

### Get Categories
```
>>> python store.py categories

{'id': 'G000046957', 'translation_id': 'MIDS_SAPPS_BUTTON_LEISURE_PUZZLES', 'name': 'Puzzle', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0134/uploadfile_20190212013457076.png', 'watch_face': False, 'content_id': '0000005171'}
{'id': 'G000046960', 'translation_id': 'MIDS_SAPPS_BUTTON_ONLINE_GAMES', 'name': 'Online Game', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0135/uploadfile_20190212013557731.png', 'watch_face': False, 'content_id': '0000005172'}
{'id': 'G000046961', 'translation_id': 'MIDS_SAPPS_BUTTON_ACTION_ADVENTURE', 'name': 'Action/Adventure', 'icon_url': 'http://img.samsungapps.com/content/2019/0212/0136/uploadfile_20190212013636628.png', 'watch_face': False, 'content_id': '0000005173'}
```

### Get Category Apps
```
>>> python store.py apps G000060951 --max_apps 3

{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000006109280', 'name': 'Tiles Hop - EDM Rush Ball & Endless Music Magic', 'icon_url': 'http://img.samsungapps.com/productNew/000006109280/IconImage_20220321044524279_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 3.0, 'release_date': '2022;01;13;', 'content_type': 'game', 'guid': 'com.GamesStore3D.TilesHopEndlessMusicMagic', 'version': '2.1.1', 'version_code': '1', 'size': 52878366, 'install_size': 52878366, 'restricted_age': '0', 'developer': 'Poppy Challenge Games', 'iap_support': True}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005751609', 'name': 'Tiles Hop: EDM Rush!', 'icon_url': 'http://img.samsungapps.com/productNew/000005751609/IconImage_20210625042847048_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.0, 'release_date': '2021;06;14;', 'content_type': 'game', 'guid': 'Music.tiles.hop.hot', 'version': '1.0', 'version_code': '1', 'size': 51295176, 'install_size': 51295176, 'restricted_age': '0', 'developer': 'VODOO GAMES', 'iap_support': False}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005250051', 'name': 'Drum Pad', 'icon_url': 'http://img.samsungapps.com/productNew/000005250051/IconImage_20210121025114863_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.5, 'release_date': '2020;09;24;', 'content_type': 'game', 'guid': 'cos.appofun_samfree.drumpad', 'version': 'Drum Pad Galaxy', 'version_code': '1', 'size': 21914755, 'install_size': 21914755, 'restricted_age': '4', 'developer': 'Free Beat Maker Machine', 'iap_support': False}
```

### Get App Details
```
>>> python store.py app 'com.playrix.homescapes.samsung'

{'id': '000005514733', 'name': 'Homescapes', 'icon_url': 'http://img.samsungapps.com/productNew/000005514733/IconImage_20220505092438492_NEW_WEB_ICON.png', 'currency_symbol': '$', 'price': 0.0, 'is_discount': False, 'average_rating': 4.5, 'content_type': 'A', 'guid': 'com.playrix.homescapes.samsung', 'version': '5.3.3', 'restricted_age': '4', 'iap_support': True, 'developer': {'name': 'Playrix', 'url': 'https://www.playrix.com', 'phone': '896034189', 'address': 'RED OAK NORTH, SOUTH COUNTY BUSINESS PARK', 'representative': 'Mikhail Smachev', 'contact_first_name': 'PLR Worldwide Sales Limited'}, 'description': "Welcome to Homescapes, ...", 'release_notes': "What's new:\n- Bug fixes and improvements\n\nPlease update the game to the latest version.\n\nWEDDING MAKEOVER\n• Save Emma's wedding!\n• Change the character's style!\n• Decorate the wedding venue!\n\nKNIGHT'S TALE\n• Help William join the Knight Club and decorate the yard with medieval decorations!\n• Get the Knight's Castle decoration.\n\nALSO\n• Woolly Season! Use the Golden Ticket to get a cute little lamb!\n• Help Betty improve her smart home and meet a robot butler!", 'customer_support_email': 'homescapes@playrix.com', 'deeplink': 'samsungapps://ProductDetail/com.playrix.homescapes.samsung?session_id=W_8EE1FEC49C2C61700D7D11650B83BDEC', 'update_date': '2022.05.05', 'permissions': ['storage'], 'privacy_policy_url': 'https://www.playrix.com/privacy/index.html', 'youtube_url': 'https://www.youtube.com/embed/9FlvCL8_4r8?hd=1&rel=0&autohide=1&showinfo=0&wmode=transparent'}
```

### Get App Reviews
```
>>> python store.py reviews 000005514733 --max_reviews 3

{'text': '3vj93', 'user': 'brad**', 'updated_date': '2022.05.13', 'stars': 5.0, 'developer_responded': False}
{'text': 'I LOVE THIS GAME ❤', 'user': 'ruby**', 'updated_date': '2022.05.12', 'stars': 5.0, 'developer_responded': False}
{'text': "Ex s d3 se rex wz ee's eeeed,,\nxz\nsix zzz x", 'user': 'coya**', 'updated_date': '2022.05.12', 'stars': 5.0, 'developer_responded': False}
```
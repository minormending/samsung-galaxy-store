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
apps: List[App] = list(store.get_category_apps(category, end=3))
for app in apps:
    print(app.__dict__)
```

### Results
```
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000006109280', 'name': 'Tiles Hop - EDM Rush Ball & Endless Music Magic', 'icon_url': 'http://img.samsungapps.com/productNew/000006109280/IconImage_20220321044524279_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 3.0, 'release_date': '2022;01;13;', 'content_type': 'game', 'guid': 'com.GamesStore3D.TilesHopEndlessMusicMagic', 'version': '2.1.1', 'version_code': '1', 'size': 52878366, 'install_size': 52878366, 'restricted_age': '0', 'developer': 'Poppy Challenge Games', 'iap_support': True}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005751609', 'name': 'Tiles Hop: EDM Rush!', 'icon_url': 'http://img.samsungapps.com/productNew/000005751609/IconImage_20210625042847048_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.0, 'release_date': '2021;06;14;', 'content_type': 'game', 'guid': 'Music.tiles.hop.hot', 'version': '1.0', 'version_code': '1', 'size': 51295176, 'install_size': 51295176, 'restricted_age': '0', 'developer': 'VODOO GAMES', 'iap_support': False}
{'category_id': 'G000060951', 'category_name': 'Music', 'category_class': 'G', 'id': '000005250051', 'name': 'Drum Pad', 'icon_url': 'http://img.samsungapps.com/productNew/000005250051/IconImage_20210121025114863_NEW_WEB_ICON_135_135.png', 'currency_symbol': '$', 'price': '0.00', 'discount_price': '0.00', 'is_discount': False, 'average_rating': 4.5, 'release_date': '2020;09;24;', 'content_type': 'game', 'guid': 'cos.appofun_samfree.drumpad', 'version': 'Drum Pad Galaxy', 'version_code': '1', 'size': 21914755, 'install_size': 21914755, 'restricted_age': '4', 'developer': 'Free Beat Maker Machine', 'iap_support': False}
```
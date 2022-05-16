import argparse
from typing import Iterable

from samsung_galaxy_store import SamsungGalaxyStore, Category, AppSummary, App, Review


def main() -> None:
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
        "app", help="Get a specific app details using the guid (i.e sku)"
    )
    app_parser.add_argument(
        "guid", help="Get a specific app details using the guid (i.e sku)"
    )

    review_parser = subparsers.add_parser(
        "reviews",
        help="Get reviews for a specific app using the product id (i.e number)",
    )
    review_parser.add_argument(
        "product_id",
        help="Get reviews for a specific app using the product id (i.e number)",
    )
    review_parser.add_argument(
        "--max_reviews",
        type=int,
        default=None,
        help="Number of reviews to return for product, ordered by most recent. Default is all reviews.",
    )

    args = parser.parse_args()

    store = SamsungGalaxyStore()
    if args.command == "categories":
        for category in store.get_categories():
            print(category.json())
    elif args.command == "apps" and args.category_id:
        category: Category = Category(args.category_id, None, None, None, False, None)
        apps: Iterable[AppSummary] = store.get_category_apps(
            category, end=args.max_apps
        )
        for app in apps:
            print(app.json())
    elif args.command == "app" and args.guid:
        app: App = store.get_app_details(args.guid)
        print(app.json())
    elif args.command == "reviews" and args.product_id:
        reviews: Iterable[Review] = store.get_app_reviews(
            args.product_id, args.max_reviews
        )
        for review in reviews:
            print(review.json())


if __name__ == "__main__":
    main()

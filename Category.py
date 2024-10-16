from typing import List

class Article:
    def __init__(self, title: str):
        self.title = title

class Category:
    def __init__(self, name: str, subcategories: List['Category'] = None):
        self.name: str = name
        self.subcategories: List['Category'] = subcategories if subcategories else []

    def get_categories(self) -> List['Category']:
        return self.subcategories

    def filter_articles_by_category(self, articles: List[Article]) -> List[Article]:
        return [article for article in articles if self.name.lower() in article.title.lower()]

class CategoryManager:
    def __init__(self):
        self.categories = [
            Category(name="All Categories"),
            Category(name="Technology"),
            Category(name="Sports"),
            Category(name="Health"),
            Category(name="Business"),
            Category(name="Entertainment"),
            Category(name="Science"),
            Category(name="World"),
            Category(name="Politics"),
            Category(name="Travel"),
            Category(name="Education")
        ]

    def get_all_categories(self) -> List[Category]:
        return self.categories

    def filter_articles(self, articles: List[Article], category_name: str) -> List[Article]:
        if category_name == "All Categories":
            return articles
        category = next((cat for cat in self.categories if cat.name == category_name), None)
        if category:
            return category.filter_articles_by_category(articles)
        return []

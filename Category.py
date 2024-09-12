
from typing import List

class Article:
    def __init__(self, title: str):
        self.title = title

class Category:
    def __init__(self, name: str, subcategories: List['Category']):
        self.name: str = name
        self.subcategories: List['Category'] = subcategories

    def get_categories(self) -> List['Category']:
        return self.subcategories

    def filter_articles_by_category(self, articles: List[Article]) -> List[Article]:
        return [article for article in articles if self.name in article.title]

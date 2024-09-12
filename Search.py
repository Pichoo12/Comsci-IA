
from datetime import date
from typing import List

class Article:
    def __init__(self, title: str, publication_date: date):
        self.title = title
        self.publication_date = publication_date

class Search:
    def __init__(self, search: str, filter_date: date):
        self.search: str = search
        self.filter_date: date = filter_date

    def filter_by_date(self, articles: List[Article], filter_date: date) -> List[Article]:
        return [article for article in articles if article.publication_date == filter_date]

    def search_articles(self, articles: List[Article], query: str) -> List[Article]:
        return [article for article in articles if query.lower() in article.title.lower()]

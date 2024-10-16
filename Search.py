from datetime import date
from typing import List

class Article:
    def __init__(self, title: str, publication_date: date):
        self.title = title
        self.publication_date = publication_date

class Search:
    def __init__(self):
        pass

    def filter_out_characters(self, articles: List[Article], chars_to_filter: str) -> List[Article]:
        # Remove specified characters from the article titles
        filtered_articles = []
        for article in articles:
            cleaned_title = ''.join([c for c in article.title if c not in chars_to_filter])
            filtered_articles.append(Article(cleaned_title, article.publication_date))
        return filtered_articles

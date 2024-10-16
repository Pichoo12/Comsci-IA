# Article.py
import requests
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QTextEdit
from typing import List

class Article:
    def __init__(self, title: str, description: str):
        self.title = title if title else "No Title"
        self.description = description if description else "No Description"

class ArticleDetailsDialog(QDialog):
    def __init__(self, article):
        super().__init__()
        self.setWindowTitle(article.title)
        layout = QVBoxLayout()
        description_label = QTextEdit(article.description)
        description_label.setReadOnly(True)
        layout.addWidget(description_label)
        self.setLayout(layout)

class ArticleManager:
    def __init__(self):
        self.api_key = 'a89636eedcc04d80b55755b5531abcd4'  # Replace with your actual News API key
        self.articles = []

    def fetch_articles(self) -> List[Article]:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={self.api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            articles_data = data.get('articles', [])
            self.articles = [
                Article(
                    title=article.get('title'),
                    description=article.get('description')
                ) for article in articles_data
            ]
            return self.articles
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch articles: {e}")

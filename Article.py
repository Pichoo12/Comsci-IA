import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit
from typing import List

class Article:
    def __init__(self, title: str, description: str, category: str = "General"):
        self.title = title
        self.description = description
        self.category = category

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
        self.api_key = 'a89636eedcc04d80b55755b5531abcd4'
        self.articles = []

    def fetch_articles(self, max_pages: int = 5) -> List[Article]:
        # Using pagination to get more articles, with a maximum of `max_pages` pages.
        self.articles = []  # Clear previously fetched articles

        for page in range(1, max_pages + 1):
            url = f'https://newsapi.org/v2/top-headlines?country=us&pageSize=100&page={page}&apiKey={self.api_key}'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Add new articles to the existing list
                new_articles = [
                    Article(
                        title=article_data.get('title', 'No Title'),
                        description=article_data.get('description', 'No Description'),
                        category=self.determine_category(article_data)
                    )
                    for article_data in data.get('articles', [])
                ]

                # Append newly fetched articles to the existing list
                self.articles.extend(new_articles)

                # If the number of articles fetched is less than requested page size, break the loop
                if len(new_articles) < 300:
                    break

            except requests.exceptions.RequestException as e:
                print(f"Error fetching articles: {e}")
                break

        return self.articles

    def fetch_articles_by_category(self, category: str) -> List[Article]:
        if category == "All Categories":
            return self.articles
        return [article for article in self.articles if article.category == category]

    def determine_category(self, article_data) -> str:
        title = article_data.get('title', '').lower()
        if "technology" in title:
            return "Technology"
        elif "sports" in title:
            return "Sports"
        elif "health" in title:
            return "Health"
        elif "business" in title:
            return "Business"
        elif "entertainment" in title:
            return "Entertainment"
        elif "science" in title:
            return "Science"
        else:
            return "General"


from typing import List

class Article:
    def __init__(self, title: str):
        self.title = title

class User:
    def __init__(self, user_id: int, points: int, username: str, password: str, email: str, saved_articles: List[Article]):
        self.user_id: int = user_id
        self.points: int = points
        self.username: str = username
        self.password: str = password
        self.email: str = email
        self.saved_articles: List[Article] = saved_articles
        self.logged_in: bool = False

    def login(self, username: str, password: str) -> bool:
        if self.username == username and self.password == password:
            self.logged_in = True
            return True
        return False

    def logout(self) -> None:
        self.logged_in = False

    def save_article(self, article: Article) -> None:
        self.saved_articles.append(article)

    def share_article(self, article: Article) -> None:
        print(f"Article '{article.title}' shared by {self.username}.")





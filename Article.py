class Article:
    def __init__(self, article_id: int, title: str, content: str, date: date, category: str, related_articles: List['Article'], url: str):
        self.article_id: int = article_id
        self.title: str = title
        self.content: str = content
        self.date: date = date
        self.category: str = category
        self.related_articles: List['Article'] = related_articles
        self.url: str = url

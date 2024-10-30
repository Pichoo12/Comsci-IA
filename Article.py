
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel, QPushButton, QMessageBox
from typing import List


class Article:
   def __init__(self, title: str, description: str, content: str, url: str, category: str = "General"):
       self.title = title
       self.description = description
       self.content = content 
       self.url = url  
       self.category = category


class ArticleDetailsDialog(QDialog):
   def __init__(self, article, current_user):
       super().__init__()
       self.article = article
       self.current_user = current_user
       self.setWindowTitle(article.title)
       layout = QVBoxLayout()

       description_label = QTextEdit(f"Description: {article.description}\n\nContent: {article.content}")
       description_label.setReadOnly(True)
       layout.addWidget(description_label)


       if article.url:
           url_label = QLabel(f'<a href="{article.url}">Read Full Article</a>')
           url_label.setOpenExternalLinks(True)  
           layout.addWidget(url_label)

       send_email_button = QPushButton("Send to Email")
       send_email_button.clicked.connect(self.send_email)
       layout.addWidget(send_email_button)

       save_article_button = QPushButton("Save Article")
       save_article_button.clicked.connect(self.save_article)
       layout.addWidget(save_article_button)


       self.setLayout(layout)


   def send_email(self):
       try:
           sender_email = "your_email@gmail.com"  
           sender_password = "your_password"  
           recipient_email = self.current_user.email


           subject = f"Article: {self.article.title}"
           body = f"Description: {self.article.description}\n\nContent: {self.article.content}\n\nRead Full Article: {self.article.url}"

           msg = MIMEMultipart()
           msg['From'] = sender_email
           msg['To'] = recipient_email
           msg['Subject'] = subject
           msg.attach(MIMEText(body, 'plain'))

           server = smtplib.SMTP('smtp.gmail.com', 587)
           server.starttls()
           server.login(sender_email, sender_password)
           text = msg.as_string()
           server.sendmail(sender_email, recipient_email, text)
           server.quit()


           QMessageBox.information(self, "Success", f"Article sent to {recipient_email}")


       except Exception as e:
           QMessageBox.critical(self, "Error", f"Failed to send email: {str(e)}")


   def save_article(self):
       if self.current_user:
           self.current_user.save_article(self.article)
           QMessageBox.information(self, "Success", f"Article saved to your account!")
       else:
           QMessageBox.critical(self, "Error", "You must be logged in to save an article.")




class ArticleManager:
   def __init__(self):
       self.api_key = 'a89636eedcc04d80b55755b5531abcd4' 
       self.articles = []
       self.categories = ["general", "technology", "sports", "health", "business", "entertainment", "science"]  


   def fetch_articles(self, max_pages_per_category: int = 5) -> List[Article]:
       """
       Fetches articles from multiple categories and multiple pages per category.
       This increases the total number of articles fetched.
       """
       self.articles = []


       for category in self.categories:
           for page in range(1, max_pages_per_category + 1):
               url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=100&page={page}&apiKey={self.api_key}'
               try:
                   response = requests.get(url)
                   response.raise_for_status()
                   data = response.json()


                   new_articles = [
                       Article(
                           title=article_data.get('title', 'No Title'),
                           description=article_data.get('description', 'No Description'),
                           content=article_data.get('content', 'No Content Available'),
                           url=article_data.get('url', 'No URL Available'),
                           category=category
                       )
                       for article_data in data.get('articles', [])
                   ]


                   self.articles.extend(new_articles)

                   if len(new_articles) < 100:
                       break


               except requests.exceptions.RequestException as e:
                   print(f"Error fetching articles from category {category}: {e}")
                   break


       return self.articles


   def fetch_articles_by_category(self, category: str) -> List[Article]:
       """
       Filter articles by a specific category.
       """
       if category == "All Categories":
           return self.articles
       return [article for article in self.articles if article.category.lower() == category.lower()]





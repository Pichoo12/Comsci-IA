import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from typing import List

class Article:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

class User:
    def __init__(self, user_id: int, points: int, username: str, password: str, email: str, saved_articles: List[Article] = None):
        self.user_id: int = user_id
        self.points: int = points
        self.username: str = username
        self.password: str = password
        self.email: str = email
        self.saved_articles: List[Article] = saved_articles if saved_articles else []
        self.logged_in: bool = False

    def login(self, username: str, password: str) -> bool:
        if self.username == username and self.password == password:
            self.logged_in = True
            return True
        return False

    def logout(self) -> None:
        self.logged_in = False

# Sample database of users
users_db = []

class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_user = None

    def initUI(self):
        self.setWindowTitle("Login/Register System")
        self.setGeometry(100, 100, 400, 400)

        # Set background color to blue
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('blue'))
        self.setPalette(palette)

        self.stacked_widget = QStackedWidget()

        # Login Page
        self.login_page = QWidget()
        self.login_layout = QVBoxLayout()
        self.login_page.setLayout(self.login_layout)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")
        self.login_layout.addWidget(self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_layout.addWidget(self.login_password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_register_page)
        self.login_layout.addWidget(self.register_button)

        # Register Page
        self.register_page = QWidget()
        self.register_layout = QVBoxLayout()
        self.register_page.setLayout(self.register_layout)

        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Username")
        self.register_layout.addWidget(self.register_username)

        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Password")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_layout.addWidget(self.register_password)

        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Email")
        self.register_layout.addWidget(self.register_email)

        self.submit_register_button = QPushButton("Register")
        self.submit_register_button.clicked.connect(self.register_user)
        self.register_layout.addWidget(self.submit_register_button)

        self.back_to_login_button = QPushButton("Back to Login")
        self.back_to_login_button.clicked.connect(self.open_login_page)
        self.register_layout.addWidget(self.back_to_login_button)

        # Main Page
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_page.setLayout(self.main_layout)

        self.main_label = QLabel("Welcome to the main page!")
        self.main_layout.addWidget(self.main_label)

        self.articles_text = QTextEdit()
        self.articles_text.setReadOnly(True)
        self.main_layout.addWidget(self.articles_text)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.main_layout.addWidget(self.logout_button)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.setCurrentWidget(self.login_page)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        for user in users_db:
            if user.login(username, password):
                self.current_user = user
                QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
                self.display_articles()
                self.stacked_widget.setCurrentWidget(self.main_page)
                return

        QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

    def open_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def open_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def register_user(self):
        username = self.register_username.text().strip()
        password = self.register_password.text().strip()
        email = self.register_email.text().strip()

        if username and password and email:
            user_id = len(users_db) + 1
            new_user = User(user_id=user_id, points=0, username=username, password=password, email=email)
            users_db.append(new_user)
            QMessageBox.information(self, "Registration Successful", "You have successfully registered!")
            self.open_login_page()
        else:
            QMessageBox.critical(self, "Registration Failed", "All fields are required.")

    def logout(self):
        if self.current_user:
            self.current_user.logout()
            self.current_user = None
        self.stacked_widget.setCurrentWidget(self.login_page)

    def display_articles(self):
        # Replace 'YOUR_API_KEY' with your actual News API key
        api_key = 'a89636eedcc04d80b55755b5531abcd4'
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                articles_text = ""
                for article_data in articles:
                    title = article_data.get('title', 'No Title')
                    description = article_data.get('description', 'No Description')
                    articles_text += f"Title: {title}\nDescription: {description}\n\n"

                self.articles_text.setText(articles_text)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch articles: {data.get('message', 'Unknown error')}.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch articles: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())
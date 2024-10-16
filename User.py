import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QListWidget, QListWidgetItem, QFrame
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from typing import List
from Article import Article, ArticleDetailsDialog, ArticleManager

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

# File to store user data
USER_DATA_FILE = 'users.json'

# Load users from JSON file
def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users_data = json.load(file)
            for user_data in users_data:
                user = User(
                    user_id=user_data['user_id'],
                    points=user_data['points'],
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email'],
                    saved_articles=[Article(title=article['title'], description=article.get('description', '')) for article in user_data.get('saved_articles', [])]
                )
                users_db.append(user)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

# Save users to JSON file
def save_users():
    users_data = []
    for user in users_db:
        users_data.append({
            'user_id': user.user_id,
            'points': user.points,
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'saved_articles': [{'title': article.title, 'description': article.description} for article in user.saved_articles]
        })
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users_data, file, indent=4)


class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_user = None
        self.article_manager = ArticleManager()  # Create an instance of ArticleManager
        load_users()

    def initUI(self):
        self.setWindowTitle("Login/Register System")
        self.setGeometry(100, 100, 600, 800)

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
        self.main_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.main_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.main_label)

        self.articles_list = QListWidget()
        self.articles_list.itemClicked.connect(self.show_article_details)
        self.main_layout.addWidget(self.articles_list)

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
            # Check if username or email already exists
            for user in users_db:
                if user.username == username or user.email == email:
                    QMessageBox.critical(self, "Registration Failed", "Username or email already exists.")
                    return

            user_id = len(users_db) + 1
            new_user = User(user_id=user_id, points=0, username=username, password=password, email=email)
            users_db.append(new_user)
            save_users()
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
        try:
            articles = self.article_manager.fetch_articles()
            self.articles_list.clear()
            self.article_objects = []

            for article in articles:
                title = article.title
                description = article.description
                self.article_objects.append(article)

                item = QListWidgetItem()
                item.setText(f"Title: {title}\n\nDescription: {description[:100]}...\n")
                item.setFont(QFont('Arial', 12))
                item.setSizeHint(item.sizeHint() * 1.5)
                item.setTextAlignment(Qt.AlignLeft)
                item.setBackground(QColor(240, 240, 240))
                self.articles_list.addItem(item)

                separator = QListWidgetItem()
                separator.setFlags(Qt.NoItemFlags)
                separator.setSizeHint(item.sizeHint() * 0.3)
                frame = QFrame()
                frame.setFrameShape(QFrame.HLine)
                frame.setFrameShadow(QFrame.Sunken)
                self.articles_list.addItem(separator)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_article_details(self, item):
        for article in self.article_objects:
            if item.text().startswith(f"Title: {article.title}"):
                dialog = ArticleDetailsDialog(article)
                dialog.exec_()
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())
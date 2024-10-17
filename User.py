import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QComboBox, QListWidget, QListWidgetItem, QHBoxLayout, QCalendarWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QMovie
from PyQt5.QtCore import Qt
from typing import List
from datetime import datetime
from Article import Article, ArticleDetailsDialog, ArticleManager
from Calendar import Calendar, Event

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
                    saved_articles=[Article(title=article['title']) for article in user_data.get('saved_articles', [])]
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
            'saved_articles': [{'title': article.title} for article in user.saved_articles]
        })
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users_data, file, indent=4)


class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_user = None
        self.article_manager = ArticleManager()
        load_users()

        # Initialize calendar and holidays
        holidays = [
    Event(name="New Year's Day", date="2024-01-01"),
    Event(name="Martin Luther King Jr. Day", date="2024-01-15"),
    Event(name="Valentine's Day", date="2024-02-14"),
    Event(name="Presidents' Day", date="2024-02-19"),
    Event(name="St. Patrick's Day", date="2024-03-17"),
    Event(name="Good Friday", date="2024-03-29"),
    Event(name="Easter Sunday", date="2024-03-31"),
    Event(name="Earth Day", date="2024-04-22"),
    Event(name="Labor Day (International)", date="2024-05-01"),
    Event(name="Mother's Day", date="2024-05-12"),
    Event(name="Memorial Day", date="2024-05-27"),
    Event(name="Father's Day", date="2024-06-16"),
    Event(name="Independence Day", date="2024-07-04"),
    Event(name="Labor Day (US)", date="2024-09-02"),
    Event(name="Columbus Day", date="2024-10-14"),
    Event(name="Halloween", date="2024-10-31"),
    Event(name="Veterans Day", date="2024-11-11"),
    Event(name="Thanksgiving", date="2024-11-28"),
    Event(name="Hanukkah Begins", date="2024-12-25"),
    Event(name="Christmas Day", date="2024-12-25"),
    Event(name="Boxing Day", date="2024-12-26"),
    Event(name="New Year's Eve", date="2024-12-31")
]

        self.calendar = Calendar(events=[], holidays=holidays)

    def initUI(self):
        self.setWindowTitle("News App")
        #self.setGeometry(100, 100, 600, 800)
        self.setFixedSize(400, 400)

        # Set background color to blue
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('blue'))
        self.setPalette(palette)

        self.stacked_widget = QStackedWidget()

        # Login Page
        self.login_page = QWidget()
        self.login_layout = QVBoxLayout()
        self.login_page.setLayout(self.login_layout)

        login_title = QLabel("News App")
        login_title.setFont(QFont("Arial", 24, QFont.Bold))
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setStyleSheet("color: white; margin-top: 5px; margin-bottom: 5px;")  # Decrease space above and below title
        self.login_layout.addWidget(login_title)

        login_gif = QLabel()
        login_movie = QMovie("background.gif")
        login_gif.setMovie(login_movie)
        login_movie.start()
        login_gif.setAlignment(Qt.AlignCenter)
        self.login_layout.addWidget(login_gif)

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

        self.login_layout.setSpacing(10)

        # Register Page
        self.register_page = QWidget()
        self.register_layout = QVBoxLayout()
        self.register_page.setLayout(self.register_layout)

        register_title = QLabel("News App")
        register_title.setFont(QFont("Arial", 24, QFont.Bold))
        register_title.setAlignment(Qt.AlignCenter)
        register_title.setStyleSheet("color: white; margin-top: 10px; margin-bottom: 5px;")  # Decrease space above and below title
        self.register_layout.addWidget(register_title)

        register_gif = QLabel()
        register_movie = QMovie("background.gif")
        register_gif.setMovie(register_movie)
        register_movie.start()
        register_gif.setAlignment(Qt.AlignCenter)
        self.register_layout.addWidget(register_gif)

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

        self.register_layout.setSpacing(10)

        # Main Page
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout()

        # Add Icon to top-right corner
        main_top_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("Icon.PNG").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        main_top_layout.addStretch()
        main_top_layout.addWidget(icon_label)
        self.main_layout.addLayout(main_top_layout)

        self.main_page.setLayout(self.main_layout)

        self.main_label = QLabel("Welcome to the main page!")
        self.main_layout.addWidget(self.main_label)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for articles...")
        self.search_bar.textChanged.connect(self.search_articles)  # Connect search bar to the search function
        self.main_layout.addWidget(self.search_bar)

        # Category Dropdown
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItem("All Categories")
        self.category_dropdown.addItem("Technology")
        self.category_dropdown.addItem("Sports")
        self.category_dropdown.addItem("Health")
        self.category_dropdown.addItem("Business")
        self.category_dropdown.addItem("Entertainment")
        self.category_dropdown.addItem("Science")
        self.category_dropdown.currentIndexChanged.connect(self.filter_articles_by_category)
        self.main_layout.addWidget(self.category_dropdown)

        # Calendar Button
        self.calendar_button = QPushButton("Show Next Holiday")
        self.calendar_button.clicked.connect(self.show_calendar)
        self.main_layout.addWidget(self.calendar_button)

        # Article List
        self.articles_list = QListWidget()
        self.articles_list.itemClicked.connect(self.show_article_details)
        self.main_layout.addWidget(self.articles_list)

        # Logout Button
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
        articles = self.article_manager.fetch_articles()
        self.filtered_articles = articles
        self.show_articles(articles)

    def filter_articles_by_category(self):
        selected_category = self.category_dropdown.currentText()
        if selected_category == "All Categories":
            filtered_articles = self.article_manager.fetch_articles()
        else:
            filtered_articles = self.article_manager.fetch_articles_by_category(selected_category)
        self.show_articles(filtered_articles)

    def search_articles(self):
        query = self.search_bar.text().strip().lower()
        filtered_articles = [
            article for article in self.filtered_articles
            if query in article.title.lower()
        ]
        self.show_articles(filtered_articles)

    def show_articles(self, articles):
        self.articles_list.clear()
        for article in articles:
            item = QListWidgetItem(article.title)
            self.articles_list.addItem(item)

    def show_article_details(self, item):
        for article in self.filtered_articles:
            if article.title == item.text():
                dialog = ArticleDetailsDialog(article)
                dialog.exec_()
                break

    def show_calendar(self):
        next_holiday = self.calendar.get_next_upcoming_holiday()
        if next_holiday:
            QMessageBox.information(self, "Next Holiday", f"The next holiday is {next_holiday.name} on {next_holiday.date.strftime('%Y-%m-%d')}.")
        else:
            QMessageBox.information(self, "Next Holiday", "There are no upcoming holidays.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())
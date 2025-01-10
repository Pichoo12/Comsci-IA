from typing import List
from datetime import datetime

class Event:
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = datetime.strptime(date, '%Y-%m-%d')

class Calendar:
    def __init__(self, events: List[Event], holidays: List[Event]):
        self.events: List[Event] = events
        self.holidays: List[Event] = holidays

    def notify_event(self) -> None:
        print("Notification: You have upcoming events!")

    def get_calendar(self) -> List[Event]:
        return self.events + self.holidays

    def get_next_upcoming_holiday(self) -> Event:
        today = datetime.now()
        upcoming_holidays = [holiday for holiday in self.holidays if holiday.date >= today]
        if not upcoming_holidays:
            return None
        return min(upcoming_holidays, key=lambda x: x.date)

    def highlight_next_holiday(self, calendar_widget) -> None:
        # upcoming holiday
        next_holiday = self.get_next_upcoming_holiday()
        if next_holiday:
            # Formatting
            next_holiday_date = next_holiday.date
            qdate = QDate(next_holiday_date.year, next_holiday_date.month, next_holiday_date.day)
            
            # date on the calendar
           # highlight_format = QTextCharFormat()
           # highlight_format.setBackground(QBrush(Qt.yellow))
           # highlight_format.setForeground(QBrush(Qt.red))
          #  calendar_widget.setDateTextFormat(qdate, highlight_format)

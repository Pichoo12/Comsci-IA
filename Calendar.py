from typing import List

class Event:
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date

class Calendar:
    def __init__(self, events: List[Event], holidays: List[Event]):
        self.events: List[Event] = events
        self.holidays: List[Event] = holidays

    def notify_event(self) -> None:
        print("Notification: You have upcoming events!")

    def get_calendar(self) -> List[Event]:
        return self.events + self.holidays


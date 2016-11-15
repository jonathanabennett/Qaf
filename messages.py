import curses
import attr


class Message():
    """The Message is text and a time. It is used to simplify merging."""

    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message
        self.count = 1

    def merge_message(self,other):
        if self.message == other.message:
            if self.timestamp > other.timestamp:
                self.timestamp = other.timestamp
            self.count += 1
        else return False
@attr.s
class MessageWindow():
    """The MessageWindow handles the sorting, combining, and display of
    messages."""

    window = attr.ib()
    message_list = attr.ib()

    def sort_messages(self):
        for time, message in messages:
            if 

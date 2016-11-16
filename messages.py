import curses
import attr


class Message():
    """The Message is text and a time. It is used to simplify merging."""

    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message
        self.count = 1
        self.displayed = False
        self.on_screen = False

    def merge_message(self,other):
        if self.message == other.message:
            if self.timestamp > other.timestamp:
                self.timestamp = other.timestamp
                self.count += 1
        else: return False

    def __str__(self):
        if count > 1:
            return "%s: %s x%s" % (self.timestamp, self.message, self.count)
        else: return "%s: %s" % (self.timestamp, self.message)

@attr.s
class MessageWindow():
    """The MessageWindow handles the sorting, combining, and display of
    messages."""

    window = attr.ib()
    message_list = attr.ib()

    def new_message(self, msg):
        if self.message_list[-1].merge_message(msg):
            return True
        else:
            self.message_list.append(msg)
            return True

    def update_messages(self):
        if len(self.message_list) < self.window.getmaxyx[0]:
            for line, message in enumerate(self.message_list):
                self.window.addstr(line, 1, str(message))
                message.displayed = True
                message.on_screen = True
                self.window.refresh()
                return True

        else:
            for line, message in enumerate(self.message_list[-9:]):
                self.window.addstr(line,1,str(message))
                message.displayed = True
                message.on_screen = True
                self.window.refresh()
                return True

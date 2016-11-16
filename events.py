import heapq

class EventHandler():
    """An Event describes something that happens next. It will determine whose
    turn it is to act, as well as things that happen on a tick such as
    poison."""

    def __init__(self,game):
        self.game = game
        self.event_heap = [] #Events are defined as (f_timestamp, e_event)
        self.clock = 0

    def tick(self):
        t, event = heapq.heappop(self.event_heap)
        self.clock = t
        return event

    def add_event(self, timestamp, event):
        heapq.heappush(self.event_heap, (timestamp,event))
        return True

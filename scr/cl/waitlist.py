from queue import Queue
from scr.data.passengers_data import waitlisted_passengers


class Waitlist:
    def __init__(self):
        self.seats_waitlist = Queue()  # A FIFO queue to manage the waitlist
        self.waitlisted_passengers = Queue(waitlisted_passengers)
        self.passenger = []

    def add_to_waitlist(self, passenger):
        self.seats_waitlist.put(passenger)
        passenger.booking_status = "Waitlisted"

    def remove_from_waitlist(self):
        if not self.seats_waitlist.empty():
            passenger = self.seats_waitlist.get()
            passenger.booking_status = None
            return passenger
        return None

    def get_next_in_line(self):
        return self.seats_waitlist.queue[0] if not self.seats_waitlist.empty() else None
    
    def is_on_waitlist(self, passenger_id):
        return any(passenger.passenger_id == passenger_id for passenger in self.seats_waitlist.queue)
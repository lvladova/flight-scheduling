#from cl.waitlist import Waitlist as waitlist
from scr.data.passengers_data import confirmed_passengers, waitlisted_passengers


class Passenger:
    def __init__(self, passenger_id, flight_number, departure_airport, arrival_airport, departure_date):
        self.passenger_id = passenger_id
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_date = departure_date
        self.seats = []  # List to hold Seat objects if already implemented
        self.passengers = [confirmed_passengers, waitlisted_passengers]  # List to hold Passenger objects
        #self.waitlist = waitlist  # Assuming Waitlist is already implemented
        self.left = None
        self.right = None

    def add_passenger(self, passenger):
        """Adds a passenger to the flight if not already booked."""
        if passenger not in self.passengers:
            self.passengers.append(passenger)
            # Optionally handle seat assignment here or in a separate method

    def find_available_seat(self, seat_class):
        """Find and return an available seat of the specified class, None if full."""
        for seat in self.seats:
            if not seat.is_occupied and seat.class_type == seat_class:
                return seat
        return None

    def book_flight(self, flight, seat):
        # Update booking status and seat assignment
        self.booking_status = "Booked"
        self.seat_number = seat.seat_number
        self.flight_number = flight.flight_number

    def cancel_flight(self, flight_number):
        # Update booking status to None
        self.booking_status = None
        self.seat_number = None
        self.flight_number = None

    def waitlist_flight(self, flight):
        # Update booking status to "Waitlisted"
        self.booking_status = "Waitlisted"

    def is_booked(self, flight_number):
        return self.booking_status == "Booked" and self.flight_number == flight_number
    
    def is_waitlisted(self, flight_number):
        return self.booking_status == "Waitlisted" and self.flight_number == flight_number

    def get_name(passenger):
        return passenger.name

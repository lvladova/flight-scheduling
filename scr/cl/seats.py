from scr.cl.passengers import Passenger as passenger

class Seat:
    def __init__(self, seat_number, class_type):
        self.seat_number = seat_number
        self.class_type = class_type
        self.is_occupied = False
        self.passenger = None  # This will reference a Passenger object

    def assign_passenger(self, passenger):
        self.is_occupied = True
        self.passenger = passenger
        passenger.booking_status = 'Confirmed'

    def remove_passenger(self):
        self.is_occupied = False
        self.passenger.booking_status = 'Canceled'
        self.passenger = None
    
    def book(self, flight_number, passenger):
        passenger.book_flight(flight_number, self.seat_number)
        self.assign_passenger(passenger)

    def is_available(self, flight_number):
        return not self.is_occupied and (self.passenger is not None and self.passenger.flight_number == flight_number)
        
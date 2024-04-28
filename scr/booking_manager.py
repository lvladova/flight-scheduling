from cl.flights import Flight
from cl.passengers import Passenger
from cl.seats import Seat
from cl.waitlist import Waitlist
from cl.graph import Graph

from utulities.file_reader import read_flights_from_csv, read_passengers_from_csv
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import quick_sort, radix_sort


class BookingManager:
    def __init__(self):
        self.graph = Graph()

    def add_flight(self, flight_number, departure, arrival, date):
        flight = Flight(flight_number, departure, arrival, date)
        self.graph.add_node(flight_number, flight)

    def book_passenger(self, passenger_id, flight_number, seat_class):
        flight_node = self.graph.get_node(flight_number)
        if flight_node and not flight_node.data.is_full():
            passenger = next((p for p in flight_node.data.passengers if p.passenger_id == passenger_id), None)
            if not passenger:
                passenger = Passenger(passenger_id)
                flight_node.data.passengers.append(passenger)

            seat = flight_node.data.find_available_seat(seat_class)
            if seat:
                seat.assign_passenger(passenger)
                return f"Passenger {passenger_id} booked on flight {flight_number} in seat {seat.seat_number}."
            else:
                flight_node.data.waitlist.add_to_waitlist(passenger)
                return f"Passenger {passenger_id} added to waitlist for flight {flight_number}."
        return "Flight is full or does not exist."

def setup_flights_and_seats(flights):
    for flight in flights:
        # Populate the flight with seats
        first_class_seats = [Seat(f"1{chr(i)}", "First") for i in range(65, 70)]  # Seats 1A-1E
        business_class_seats = [Seat(f"{i}{chr(j)}", "Business") for i in range(2, 7) for j in range(65, 70)]  # Seats 2A-6E
        economy_class_seats = [Seat(f"{i}{chr(j)}", "Economy") for i in range(7, 12) for j in range(65, 70)]  # Seats 7A-11E

        # Add seats to the flight
        flight.seats.extend(first_class_seats + business_class_seats + economy_class_seats)
    return flight

def handle_waitlist(flight, waitlist):
    # Check if there is anyone on the waitlist and book them if a seat is available
    next_passenger = waitlist.get_next_in_line()
    if next_passenger:
        for seat in flight.seats:
            if not seat.is_occupied and flight.book_seat(next_passenger, seat.seat_number):
                waitlist.remove_from_waitlist()
                break




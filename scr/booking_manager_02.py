from utulities.file_reader import read_csv
from cl.flights import Flight
from cl.graph import Graph
from cl.passengers import Passenger

class BookingManager:
    def __init__(self):
        self.graph = Graph()

    def load_data(self, flights_csv, passengers_csv):
        flights_df = read_csv(flights_csv)
        passengers_df = read_csv(passengers_csv)

        for _, row in flights_df.iterrows():
            flight = Flight(row['flight_number'], row['departure_airport'], row['arrival_airport'], row['departure_date'])
            self.graph.add_node(row['flight_number'], flight)

        for _, row in passengers_df.iterrows():
            passenger = Passenger(row['passenger_id'], row['name'], row['booking_status'], row['seat_number'], row['flight_number'])
            node = self.graph.get_node(row['flight_number'])
            if node:
                # Assuming a seat number is provided in the CSV and should be assigned immediately
                seat_number = row['seat_number'] if 'seat_number' in row else None
                if seat_number:
                    node.data.add_passenger(passenger, seat_number)

    def add_flight(self, flight_number, departure, arrival, date):
        flight = Flight(flight_number, departure, arrival, date)
        self.graph.add_node(flight_number, flight)

    def book_passenger(self, flight_number, passenger_id, seat_class):
        node = self.graph.get_node(flight_number)
        if node:
            return node.data.book_seat(passenger_id, seat_class)
        return "Flight not found."

    def cancel_booking(self, flight_number, passenger_id):
        flight = self.graph.get_node(flight_number).data
        passenger = next((p for p in flight.passengers if p.passenger_id == passenger_id), None)
        return flight.cancel_passenger(passenger)

    def get_flight_info(self, flight_number):
        flight = self.graph.get_node(flight_number).data
        return flight.get_flight_info()

    def get_passenger_status(self, passenger_id):
        for node in self.graph.nodes.values():
            flight = node.data
            for seat_class, seats in flight.seats.items():
                for seat in seats:
                    if seat.passenger and seat.passenger.passenger_id == passenger_id:
                        return f"{passenger_id} is booked on Flight {flight.flight_number} in {seat_class} class."
                if passenger_id in [p.passenger_id for p in flight.waitlists[seat_class]]:
                    return f"{passenger_id} is on the waitlist for Flight {flight.flight_number} in {seat_class} class."

    def manage_waitlist(self, flight_number):
        node = self.graph.get_node(flight_number)
        if node:
            return node.data.handle_waitlist()

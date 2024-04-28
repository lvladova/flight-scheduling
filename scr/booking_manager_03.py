import streamlit as st
from collections import deque

from data.passengers_data import confirmed_passengers, waitlisted_passengers
from data.flights_pile import flights as flights
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import merge_sort
from cl.graph import Graph





class BookingManager:
    def __init__(self, flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack, confirmed_passengers_stack, waitlisted_passengers_queue):
        self.flights_graph = flights_graph
        self.passengers_graph = passengers_graph
        self.flights_table = flights_table
        self.passengers_tree = passengers_tree
        self.flights_stack = flights_stack
        self.confirmed_passengers_stack = confirmed_passengers_stack
        self.waitlisted_passengers_queue = waitlisted_passengers_queue


    def book_passenger(self, passenger, flight_number):
        """ Attempt to book a passenger on a specific flight """
        # Attempt to book using the graph and stack for LIFO behavior
        found_flight = None
        for flight in self.flights_table.search_by_flight_number(flight_number):  # Use the hash table for efficient searching
            if flight[0] == flight_number and len(flight[4]) > 0:
                found_flight = flight
                break

        if found_flight:
            seat = found_flight[4].pop()  # Remove the last seat (LIFO)
            passenger.append(seat)
            self.confirmed_passengers_stack.append(passenger)
            flight_node = self.flights_graph.get_node(flight_number)
            passenger_node = self.passengers_graph.get_node(passenger[0])
            if flight_node is not None and passenger_node is not None:
                flight_node.add_data(passenger)  # Add the passenger data to the flight node
                passenger_node.add_data(flight_number)  # Add the flight data to the passenger node
            print(f"Passenger {passenger[1]} booked on flight {flight_number} with seat number {seat}.")
            return True

        # No seats available, add to the queue
        self.waitlisted_passengers_queue.append(passenger)
        print(f"Passenger {passenger[1]} added to waitlist for flight {flight_number}.")
        return False
    
    def cancel_booking(self, passenger_id, flight_number):
        """ Cancel a booking and manage the graph """
        found = False
        temp_stack = []
        while self.confirmed_passengers_stack:
            passenger = self.confirmed_passengers_stack.pop()
            if passenger[0] == passenger_id and passenger[4] == flight_number:
                found = True
                for flight in self.flights_table.search_by_flight_number(flight_number):  # Use the hash table for efficient searching
                    if flight[0] == flight_number:
                        flight[4].append(passenger[3])  # Return the seat to the flight stack
                        break
                flight_node = self.flights_graph.get_node(flight_number)
                passenger_node = self.passengers_graph.get_node(passenger_id)
                if flight_node is not None and passenger_node is not None:
                    flight_node.remove_data(passenger)  # Remove the passenger data from the flight node
                    passenger_node.remove_data(flight_number)  # Remove the flight data from the passenger node
                print(f"Booking cancelled for {passenger[1]} from flight {flight_number}.")
                break
            temp_stack.append(passenger)

        while temp_stack:
            self.confirmed_passengers_stack.append(temp_stack.pop())

        return found

    def manage_waitlist(self, flight_number):
        """ Attempt to book waitlisted passengers on a specific flight """
        found_flight = None
        for flight in reversed(self.flights_stack):  # Check the most recently added flights first
            if flight[0] == flight_number and len(flight[4]) > 0:
                found_flight = flight
                break

        if found_flight:
            temp_queue = deque()  # Temporary queue to hold passengers not waitlisted for this flight
            while self.waitlisted_passengers_queue and len(found_flight[4]) > 0:
                passenger = self.waitlisted_passengers_queue.popleft()
                if passenger[3] != flight_number:  # If the passenger is not waitlisted for this flight
                    temp_queue.append(passenger)  # Add them to the temporary queue
                    continue  # Skip to the next passenger

                seat = found_flight[4].pop()  # Remove the last seat (LIFO)
                passenger.append(seat)
                self.confirmed_passengers_stack.append(passenger)
                flight_node = self.flights_graph.get_node(flight_number)
                passenger_node = self.passengers_graph.get_node(passenger[0])
                if flight_node is not None and passenger_node is not None:
                    flight_node.add_data(passenger)  # Add the passenger data to the flight node
                    passenger_node.add_data(flight_number)  # Add the flight data to the passenger node
                print(f"Waitlisted passenger {passenger[1]} booked on flight {flight_number} with seat number {seat}.")

            # Add back the passengers not waitlisted for this flight to the waitlist queue
            while temp_queue:
                self.waitlisted_passengers_queue.append(temp_queue.popleft())

    def get_flight_info(self, flight_number):
        node = self.flights_graph.get_node(flight_number)
        if node:
            flight_data = node.data
            return f"Flight Number: {flight_data[0]}, Departure Airport: {flight_data[1]}, Arrival Airport: {flight_data[2]}, Date and Time: {flight_data[3]}"

    def get_passenger_status(self, passenger_id):
        passenger_node = self.passengers_graph.get_node(passenger_id)
        if passenger_node:
            flights = passenger_node.data
            return f"Passenger {passenger_id} is booked: Information: {flights}."
        return f"Passenger {passenger_id} is not booked on any flight."



def main():

    flights_graph = Graph()
    passengers_graph = Graph()
    flights_table = FlightHashTable()
    passengers_tree = PassengerBST()
    flights_stack = flights
    confirmed_passengers_stack = confirmed_passengers
    waitlisted_passengers_queue = deque(waitlisted_passengers)

    # Add the flights to the flights graph
    for flight in merge_sort(flights, '0'):  # Sort by flight number
        if flight is not None and len(flight) > 0:
            flights_graph.add_node(flight[0], flight)
            flights_table.insert(flight)

    # Add the confirmed passengers to the passengers graph
    for passenger in confirmed_passengers:
        if passenger is not None and len(passenger) > 0:
            passengers_graph.add_node(passenger[0], passenger)
            passengers_tree.insert(passenger)

    for passenger in waitlisted_passengers:
        if passenger is not None and len(passenger) > 0:
            passengers_graph.add_node(passenger[0], passenger)
            passengers_tree.insert(passenger)

    manager = BookingManager(flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack, confirmed_passengers_stack, waitlisted_passengers_queue)

    manager.book_passenger([102500, "New Passenger", "Pending"], 1024)
    manager.cancel_booking(102402, 1024)

    info = manager.get_flight_info(1024)
    print(info)

    status = manager.get_passenger_status(102403)
    print(status)

    waitlist_info = manager.manage_waitlist(1026)
    print(waitlist_info)

if __name__ == '__main__':
    main()


'''    
    def manage_waitlist(self, flight_number):
        # Assuming waitlisted_passengers_queue is a queue of passengers waiting for any flight
        waitlisted_passengers = [passenger for passenger in self.waitlisted_passengers_queue if passenger[4] == flight_number]
        return f"Flight {flight_number} has {len(waitlisted_passengers)} passengers on the waitlist."


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
'''
import unittest
import time
from booking_manager_03 import BookingManager
from collections import deque
from cl.graph import Graph
from data.passengers_data import confirmed_passengers, waitlisted_passengers
from data.flights_pile import flights as flights
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import merge_sort

# Create a graph for flights and passengers
flights_graph = Graph()
passengers_graph = Graph()

# Create a hash table for flights and a binary search tree for passengers
flights_table = FlightHashTable()
passengers_tree = PassengerBST()

# Create stacks for flights, confirmed passengers, and a queue for waitlisted passengers
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

# Add the waitlisted passengers to the passengers graph
for passenger in waitlisted_passengers:
    if passenger is not None and len(passenger) > 0:
        passengers_graph.add_node(passenger[0], passenger)
        passengers_tree.insert(passenger)


class TestBookingManager(unittest.TestCase):
    def setUp(self):
        # Create an instance of BookingManager with the necessary parameters
        self.manager = BookingManager(flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack,
                                      confirmed_passengers_stack, waitlisted_passengers_queue)
        # Book passenger with ID 1 on flight 1024
        self.manager.book_passenger([1, 'John Doe', 'Pending'], 1024, 'Economy')

    def test_book_passenger_success(self):
        sizes = [10, 100, 1000, 10000]
        for size in sizes:
            start_time = time.time()
            for _ in range(size):
                # Book additional passengers on flight 1024
                self.manager.book_passenger([_+2, 'Test Passenger', 'Pending'], 1024, 'Economy')
            end_time = time.time()
            print(f"book_passenger (success) with {size} passengers took {end_time - start_time} seconds")

    def test_book_passenger_failure(self):
        sizes = [10, 100, 1000, 10000]
        for size in sizes:
            start_time = time.time()
            for _ in range(size):
                # Attempt to book additional passengers on flight 1024, but fail due to capacity constraints
                self.manager.book_passenger([_+2, 'Test Passenger', 'Pending'], 1024, 'Economy')
            end_time = time.time()
            print(f"book_passenger (failure) with {size} passengers took {end_time - start_time} seconds")

    def test_cancel_booking(self):
        start_time = time.time()
        # Cancel the booking for passenger with ID 1 on flight 1024
        result = self.manager.cancel_booking(1, 1024)
        end_time = time.time()
        print(f"cancel_booking took {end_time - start_time} seconds")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

from collections import deque
from sceduling.sorters import quick_sort, radix_sort

class BookingManager:
    def __init__(self, flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack, confirmed_passengers_stack, waitlisted_passengers_queue):
        """
        Initialize the BookingManager with the necessary data structures.
        
        Args:
        - flights_graph: Graph representing flights and their connections.
        - passengers_graph: Graph representing passengers and their flights.
        - flights_table: Hash table for efficient searching of flights.
        - passengers_tree: Binary search tree for efficient searching of passengers.
        - flights_stack: Stack to keep track of flights in LIFO order.
        - confirmed_passengers_stack: Stack to keep track of confirmed passengers in LIFO order.
        - waitlisted_passengers_queue: Queue to keep track of waitlisted passengers in FIFO order.
        """
        self.flights_graph = flights_graph
        self.passengers_graph = passengers_graph
        self.flights_table = flights_table
        self.passengers_tree = passengers_tree
        self.flights_stack = flights_stack
        self.confirmed_passengers_stack = confirmed_passengers_stack
        self.waitlisted_passengers_queue = waitlisted_passengers_queue

    def book_passenger(self, passenger, flight_number, seat_class):
        """ 
        Attempt to book a passenger on a specific flight in a specific class.
        
        Args:
        - passenger: List containing passenger information.
        - flight_number: Flight number to book the passenger on.
        - seat_class: Class of the seat to book.
        
        Returns:
        - A string indicating the booking status.
        """
        # Attempt to book using the graph and stack for LIFO behavior
        found_flight = None

        if self.is_passenger_booked_or_waitlisted(passenger[0], flight_number):
            return f"Passenger {passenger[1]} is already booked or waitlisted for flight {flight_number}."

        if not self.is_seat_class_available(flight_number, seat_class):
            return f"No available space in {seat_class} class for flight {flight_number}."

        # Use the hash table for efficient searching
        for flight in self.flights_table.search_by_flight_number(flight_number):
            if flight[0] == flight_number and len(flight[4][seat_class]) > 0:
                found_flight = flight
                break

        if found_flight:
            seat = found_flight[4][seat_class].pop()  # Remove the last seat (LIFO)
            passenger.append(seat)
            passenger.append(seat_class)  # Add the seat class to the passenger data
            self.confirmed_passengers_stack.append(passenger)
            flight_node = self.flights_graph.get_node(flight_number)
            passenger_node = self.passengers_graph.get_node(passenger[0])
            if flight_node is not None and passenger_node is not None:
                flight_node.add_data(passenger)  # Add the passenger data to the flight node
                passenger_node.add_data(flight_number)  # Add the flight data to the passenger node
            return f"Passenger {passenger[1]} booked on flight {flight_number} with seat number {seat} in {seat_class} class."

        # No seats available, add to the waitlist for the specific class
        passenger.append(seat_class)  # Add the seat class to the passenger data
        self.waitlisted_passengers_queue.append(passenger)
        return f"Passenger {passenger[1]} added to waitlist for flight {flight_number} in {seat_class} class."

    def cancel_booking(self, passenger_id, flight_number):
        """ 
        Cancel a booking and manage the graph.
        
        Args:
        - passenger_id: ID of the passenger to cancel the booking for.
        - flight_number: Flight number to cancel the booking for.
        
        Returns:
        - A boolean indicating whether the booking was found and cancelled.
        """
        found = False
        seat_class = None  # Initialize seat_class to None
        temp_stack = []
        while self.confirmed_passengers_stack:
            passenger = self.confirmed_passengers_stack.pop()
            if passenger[0] == passenger_id and passenger[4] == flight_number:
                found = True
                seat_class = passenger[-1]  # Get the seat class from the passenger data
                for flight in self.flights_table.search_by_flight_number(
                        flight_number):  # Use the hash table for efficient searching
                    if flight[0] == flight_number:
                        flight[4][seat_class].append(passenger[3])  # Return the seat to the flight stack
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

        # Check if there are passengers on the waitlist for the flight
        temp_queue = deque()
        while self.waitlisted_passengers_queue:
            passenger = self.waitlisted_passengers_queue.popleft()
            if passenger[3] == flight_number and passenger[-1] == seat_class:
                print(
                    f"Passenger {passenger[1]} is on the waitlist for flight {flight_number} in {seat_class} class. Would you like to book them?")
                # Here you can add code to handle user input and book the passenger if the user agrees
                break
            temp_queue.append(passenger)

        # Add back the passengers not waitlisted for this flight to the waitlist queue
        while temp_queue:
            self.waitlisted_passengers_queue.append(temp_queue.popleft())

        return found

    def manage_waitlist(self, flight_number):
        """
        Manage the waitlist for a specific flight.
        
        Args:
        - flight_number: Flight number to manage the waitlist for.
        
        Returns:
        - A list of strings indicating the booking status of waitlisted passengers.
        """
        found_flight = None
        messages = []
        for flight in reversed(self.flights_stack):  # Last in, first out management
            if flight[0] == flight_number:
                found_flight = flight
                break

        if found_flight:
            # Using radix_sort to prioritize waitlisted passengers by a sortable attribute
            sorted_waitlist = radix_sort(list(self.waitlisted_passengers_queue), lambda x: x[1]) 

            for passenger in sorted_waitlist:
                seat_class = passenger[-1]
                if seat_class in found_flight[4] and len(found_flight[4][seat_class]) > 0:
                    seat = found_flight[4][seat_class].pop()
                    passenger.append(seat)
                    self.confirmed_passengers_stack.append(passenger)
                    flight_node = self.flights_graph.get_node(flight_number)
                    passenger_node = self.passengers_graph.get_node(passenger[0])
                    if flight_node and passenger_node:
                        flight_node.add_data(passenger)
                        passenger_node.add_data(flight_number)
                    messages.append(f"Waitlisted passenger {passenger[1]} booked on flight {flight_number} with seat number {seat} in {seat_class} class.")
                    # Once a passenger is booked, they should be removed from the waitlist
                    self.waitlisted_passengers_queue.remove(passenger)

        return messages

    def get_flight_info(self, flight_number):
        """ 
        Get the information for a flight.
        
        Args:
        - flight_number: Flight number to get the information for.
        
        Returns:
        - A string containing the flight information.
        """
        flight_node = self.flights_graph.get_node(flight_number)
        if flight_node is not None:
            flight_data = flight_node.data
            info_lines = []
            info_lines.append(f"Flight Number: {flight_data[0]}")
            info_lines.append(f"Departure Airport: {flight_data[1]}")
            info_lines.append(f"Arrival Airport: {flight_data[2]}")
            info_lines.append(f"Date and Time: {flight_data[3]}")
            info_lines.append("Passenger Information:")

            # Collect passenger data for this flight
            passenger_info = []
            for passenger_node in self.passengers_graph.nodes.values():
                passenger_data = passenger_node.data
                if passenger_data[4] == flight_number:  
                    passenger_info.append(passenger_data)

            # Sort passenger data by seat number using quick_sort
            sorted_passenger_info = quick_sort(passenger_info, key=lambda x: x[3])  

            # Append sorted passenger info to info_lines
            for passenger in sorted_passenger_info:
                info_lines.append(f"Seat {passenger[3]}: Passenger ID: {passenger[0]}, Passenger Name: {passenger[1]}")

            return "\n".join(info_lines)
        else:
            return f"Flight {flight_number} not found."

    def get_passenger_status(self, passenger_id):
        """ 
        Get the status of a passenger.
        
        Args:
        - passenger_id: ID of the passenger to get the status for.
        
        Returns:
        - A string indicating the status of the passenger.
        """
        # Check if the passenger is booked on any flight
        for passenger in self.confirmed_passengers_stack:
            if passenger[0] == passenger_id:
                flight_number = passenger[4]
                seat_class = passenger[-1]
                flight_node = self.flights_graph.get_node(flight_number)
                if flight_node is not None:
                    flight_data = flight_node.data
                    return f"Passenger {passenger_id} is booked on Flight {flight_data[0]} from {flight_data[1]} to {flight_data[2]} at {flight_data[3]} in {seat_class} class."

        # Check if the passenger is on the waitlist for any flight
        for i, passenger in enumerate(self.waitlisted_passengers_queue):
            if passenger[0] == passenger_id:
                flight_number = passenger[3]
                seat_class = passenger[-1]
                flight_node = self.flights_graph.get_node(flight_number)
                if flight_node is not None:
                    flight_data = flight_node.data
                    return f"Passenger {passenger_id} is on the waitlist for Flight {flight_data[0]} from {flight_data[1]} to {flight_data[2]} at {flight_data[3]} in {seat_class} class. Position on waitlist: {i + 1}."

        return f"Passenger {passenger_id} is not booked on any flight or on any waitlist."

    def is_passenger_booked_or_waitlisted(self, passenger_id, flight_number):
        """ 
        Check if a passenger is already booked or waitlisted for a flight.
        
        Args:
        - passenger_id: ID of the passenger to check.
        - flight_number: Flight number to check.
        
        Returns:
        - A boolean indicating whether the passenger is already booked or waitlisted.
        """
        # Check the confirmed passengers stack
        for passenger in self.confirmed_passengers_stack:
            if passenger[0] == passenger_id and passenger[3] == flight_number:
                return True

        # Check the waitlisted passengers queue
        for passenger in self.waitlisted_passengers_queue:
            if passenger[0] == passenger_id and passenger[3] == flight_number:
                return True

        return False

    def is_seat_class_available(self, flight_number, seat_class):
        """ 
        Check if there is available space in a specific class for a flight.
        
        Args:
        - flight_number: Flight number to check.
        - seat_class: Class of the seat to check.
        
        Returns:
        - A boolean indicating whether there is available space in the class.
        """
        # Define the capacity of each class
        class_capacity = {
            "First": 10,
            "Business": 20,
            "Economy": 70
        }
        # Count the number of passengers booked in the requested class
        count = 0
        for passenger in self.confirmed_passengers_stack:
            if passenger[4] == flight_number and passenger[-1] == seat_class:
                count += 1
        # Check if there is available space in the class
        return count < class_capacity[seat_class]

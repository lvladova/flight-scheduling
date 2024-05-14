from cl.graph import Node as Node

# Hash table for searching through flights by flight number, departure airport, and arrival airport
class FlightHashTable:
    def __init__(self):
        self.table = {}

    def insert(self, flight):
        # Generate a key using flight number, departure airport, and arrival airport
        key = (flight[0], flight[1], flight[2])
        self.table[key] = flight

    def search_by_flight_number(self, flight_number):
        # Return a list of flights with matching flight number
        return [flight for flight in self.table.values() if flight[0] == flight_number]

    def search_by_departure_airport(self, departure_airport):
        # Return a list of flights with matching departure airport
        return [flight for flight in self.table.values() if flight[1] == departure_airport]

    def search_by_arrival_airport(self, arrival_airport):
        # Return a list of flights with matching arrival airport
        return [flight for flight in self.table.values() if flight[2] == arrival_airport]
    
    def get_all_flights(self):
        # Return a list of all flights in the hash table
        return list(self.table.values())


# Binary search tree for searching through passengers
class PassengerBST:
    def __init__(self):
        self.root = None

    def insert(self, passenger):
        if not self.root:
            # If the tree is empty, set the root node
            self.root = Node(passenger)
        else:
            self._insert(self.root, Node(passenger))

    def _insert(self, node, passenger_node):
        if passenger_node.data is not None and node.data is not None:
            if passenger_node.data[0] < node.data[0]:  # Use index to access the passenger ID
                if node.left is None:
                    # If the left child is None, insert the passenger node as the left child
                    node.left = passenger_node
                else:
                    # Recursively insert the passenger node in the left subtree
                    self._insert(node.left, passenger_node)
            else:
                if node.right is None:
                    # If the right child is None, insert the passenger node as the right child
                    node.right = passenger_node
                else:
                    # Recursively insert the passenger node in the right subtree
                    self._insert(node.right, passenger_node)
        else:
            return 

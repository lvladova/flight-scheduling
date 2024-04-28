from cl.graph import Node as Node

#hash table search for searching through flights by flight number, departure airport, and arrival airport
class FlightHashTable:
    def __init__(self):
        self.table = {}

    def insert(self, flight):
        key = (flight[0], flight[1], flight[2])
        self.table[key] = flight

    def search_by_flight_number(self, flight_number):
        return [flight for flight in self.table.values() if flight[0] == flight_number]

    def search_by_departure_airport(self, departure_airport):
        return [flight for flight in self.table.values() if flight[1] == departure_airport]

    def search_by_arrival_airport(self, arrival_airport):
        return [flight for flight in self.table.values() if flight[2] == arrival_airport]
    
    def get_all_flights(self):
        return list(self.table.values())


#for searching through passenger with a binary search tree
class PassengerBST:
    def __init__(self):
        self.root = None

    def insert(self, passenger):
        if not self.root:
            self.root = Node(passenger)
        else:
            self._insert(self.root, Node(passenger))

    def _insert(self, node, passenger_node):
        if passenger_node.data is not None and node.data is not None:
            if passenger_node.data[0] < node.data[0]:  # Use index to access the passenger ID
                if node.left is None:
                    node.left = passenger_node
                else:
                    self._insert(node.left, passenger_node)
            else:
                if node.right is None:
                    node.right = passenger_node
                else:
                    self._insert(node.right, passenger_node)
        else:
            return #print("Error: Node data is None")

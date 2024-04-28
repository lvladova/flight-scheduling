import streamlit as st
from booking_manager_03 import BookingManager
from cl.graph import Graph
from collections import deque
from data.passengers_data import confirmed_passengers, waitlisted_passengers
from data.flights_pile import flights as flights
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import merge_sort

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

manager = BookingManager(flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack,
                         confirmed_passengers_stack, waitlisted_passengers_queue)

st.title('Flight Booking System')

flight_number = st.text_input('Enter flight number')
passenger_id = st.text_input('Enter passenger ID')
seat_class = st.selectbox('Select seat class', ['First', 'Business', 'Economy'])

if st.button('Book Passenger'):
    result = manager.book_passenger(passenger_id, flight_number)
    st.write(result)

if st.button('Cancel Booking'):
    result = manager.cancel_booking(passenger_id, flight_number)
    if result:
        passenger_name = [p[1] for p in confirmed_passengers if p[0] == int(passenger_id)][0]
        st.success(f"Booking cancelled for {passenger_name} on flight {flight_number}")
    else:
        st.write(result)

if st.button('Get Flight Info'):
    result = manager.get_flight_info(flight_number)
    st.write(result)

if st.button('Get Passenger Status'):
    result = manager.get_passenger_status(passenger_id)
    st.write(result)

if st.button('Manage Waitlist'):
    result = manager.manage_waitlist(flight_number)
    st.write(result)

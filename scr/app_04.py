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


def book_passenger():
    if st.session_state.passenger_name and st.session_state.passenger_id and st.session_state.flight_number and st.session_state.seat_class:
        passenger_id = int(st.session_state.passenger_id)
        flight_number = int(st.session_state.flight_number)
        # Attempt to book the passenger
        success = manager.book_passenger([passenger_id, st.session_state.passenger_name, "Pending"], flight_number, st.session_state.seat_class)
        if success:
            st.success(f"Passenger {st.session_state.passenger_name} ({passenger_id}) booked on flight {flight_number} in {st.session_state.seat_class} class.")
        else:
            # If booking failed, check if the passenger is already booked or waitlisted
            if manager.is_passenger_booked_or_waitlisted(passenger_id, flight_number):
                st.error(f"Passenger {st.session_state.passenger_name} ({passenger_id}) is already booked or waitlisted for flight {flight_number}.")
            else:
                # If the passenger is not already booked or waitlisted, add the passenger to the waitlist
                manager.waitlisted_passengers_queue.append([passenger_id, st.session_state.passenger_name, "Waitlisted", flight_number, st.session_state.seat_class])
                st.success(f"Passenger {st.session_state.passenger_name} ({passenger_id}) added to waitlist for flight {flight_number} in {st.session_state.seat_class} class.")
    else:
        st.error("Please enter all the details.")


def main():
    st.title("Flight Booking System")

    st.header("Book a Passenger")
    st.text_input("Enter Passenger Name", value=st.session_state.get('passenger_name', ''), key='passenger_name')
    st.text_input("Enter Passenger ID", value=st.session_state.get('passenger_id', ''), key='passenger_id')
    st.text_input("Enter Flight Number", value=st.session_state.get('flight_number', ''), key='flight_number')
    seat_classes = ["First", "Business", "Economy"]
    st.selectbox("Choose a Class", seat_classes, index=seat_classes.index(st.session_state.get('seat_class', seat_classes[0])), key='seat_class')

    st.button("Book Passenger", on_click=book_passenger)


if __name__ == "__main__":
    main()

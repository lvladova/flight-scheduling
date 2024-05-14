import streamlit as st
from collections import deque
from booking_manager_03 import BookingManager
from cl.graph import Graph
from data.passengers_data import confirmed_passengers, waitlisted_passengers
from data.flights_pile import flights as flights
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import merge_sort

# Create graphs, tables, and stacks for flights and passengers
flights_graph = Graph()  # Graph to store flight information
passengers_graph = Graph()  # Graph to store passenger information
flights_table = FlightHashTable()  # Hash table to quickly search flights
passengers_tree = PassengerBST()  # Binary search tree to quickly search passengers
flights_stack = flights  # Stack to store flights
confirmed_passengers_stack = confirmed_passengers  # Stack to store confirmed passengers
waitlisted_passengers_queue = deque(waitlisted_passengers)  # Queue to store waitlisted passengers

# Add the flights to the flights graph
for flight in merge_sort(flights, '0'):  # Sort flights by flight number
    if flight is not None and len(flight) > 0:
        flights_graph.add_node(flight[0], flight)  # Add flight to the graph
        flights_table.insert(flight)  # Insert flight into the hash table

# Add the confirmed passengers to the passengers graph
for passenger in confirmed_passengers:
    if passenger is not None and len(passenger) > 0:
        passengers_graph.add_node(passenger[0], passenger)  # Add passenger to the graph
        passengers_tree.insert(passenger)  # Insert passenger into the binary search tree

# Add the waitlisted passengers to the passengers graph
for passenger in waitlisted_passengers:
    if passenger is not None and len(passenger) > 0:
        passengers_graph.add_node(passenger[0], passenger)  # Add passenger to the graph
        passengers_tree.insert(passenger)  # Insert passenger into the binary search tree

# Create the BookingManager and store it in the session state
if 'manager' not in st.session_state:
    st.session_state['manager'] = BookingManager(flights_graph, passengers_graph, flights_table, passengers_tree, flights_stack,
                         confirmed_passengers_stack, waitlisted_passengers_queue)
else:
    manager = st.session_state['manager']


def book_passenger():
    # Check if all the required details are entered
    if st.session_state.booking_passenger_name and st.session_state.booking_passenger_id and st.session_state.booking_flight_number and st.session_state.seat_class:
        passenger_id = int(st.session_state.booking_passenger_id)
        flight_number = int(st.session_state.booking_flight_number)

        # Check if the passenger is already booked or waitlisted
        if st.session_state['manager'].is_passenger_booked_or_waitlisted(passenger_id, flight_number):
            st.error(f"Passenger {st.session_state.booking_passenger_name} ({passenger_id}) is already booked or waitlisted for flight {flight_number}.")
        else:
            # Attempt to book the passenger
            result = st.session_state['manager'].book_passenger([passenger_id, st.session_state.booking_passenger_name, "Pending"], flight_number, st.session_state.seat_class)
            if isinstance(result, str):
                st.success(result)
            else:
                # If booking failed, add the passenger to the waitlist
                st.session_state['manager'].waitlisted_passengers_queue.append([passenger_id, st.session_state.booking_passenger_name, "Waitlisted", flight_number, st.session_state.seat_class])
                st.success(f"Passenger {st.session_state.booking_passenger_name} ({passenger_id}) added to waitlist for flight {flight_number} in {st.session_state.seat_class} class.")
    else:
        st.error("Please enter all the details.")


def cancel_passenger():
    # Check if all the required details are entered
    if st.session_state.cancellation_passenger_id and st.session_state.cancellation_flight_number:
        passenger_id = int(st.session_state.cancellation_passenger_id)
        flight_number = int(st.session_state.cancellation_flight_number)
        # Attempt to cancel the booking
        success = st.session_state['manager'].cancel_booking(passenger_id, flight_number)
        if success:
            st.success(f"Passenger {passenger_id} cancelled from flight {flight_number}.")
            # Check if there are passengers on the waitlist for the flight
            messages = st.session_state['manager'].manage_waitlist(flight_number)
            if messages:
                for message in messages:
                    st.success(message)
            else:
                st.info("No waitlisted passengers for this flight.")
        else:
            st.error(f"Could not cancel booking for passenger {passenger_id} from flight {flight_number}.")
    else:
        st.error("Please enter all the details.")


def check_passenger_status():
    # Check if the passenger ID is entered
    if st.session_state.status_passenger_id:
        passenger_id = int(st.session_state.status_passenger_id)
        status = st.session_state['manager'].get_passenger_status(passenger_id)
        if status:
            st.success(status)
        else:
            st.error(f"Passenger {passenger_id} not found.")
    else:
        st.error("Please enter the passenger ID.")


def check_flight_info():
    flight_number = st.session_state.get('flight_number')
    if flight_number:
        flight_info = st.session_state['manager'].get_flight_info(int(flight_number))
        if "not found" not in flight_info:
            st.success(f"Flight {flight_number} found.")
            if isinstance(flight_info, list):  # Check if the flight_info is a list
                for passenger in flight_info:  # Iterate over the list of passengers
                    st.text_area("Passenger Info", passenger, height=200)
            else:
                st.text_area("Flight Info", flight_info, height=200)
        else:
            st.error(flight_info)
    else:
        st.error("Please enter the flight number.")


def main():
    st.title("Flight Booking System")

    with st.expander("Book a Passenger"):
        st.text_input("Enter Passenger Name", value=st.session_state.get('booking_passenger_name', ''), key='booking_passenger_name')
        st.text_input("Enter Passenger ID", value=st.session_state.get('booking_passenger_id', ''), key='booking_passenger_id')
        st.text_input("Enter Flight Number", value=st.session_state.get('booking_flight_number', ''), key='booking_flight_number')
        seat_classes = ["First", "Business", "Economy"]
        st.selectbox("Choose a Class", seat_classes, index=seat_classes.index(st.session_state.get('seat_class', seat_classes[0])), key='seat_class')
        st.button("Book Passenger", on_click=book_passenger)

    with st.expander("Cancel a Booking"):
        st.text_input("Enter Passenger ID", value=st.session_state.get('cancellation_passenger_id', ''), key='cancellation_passenger_id')
        st.text_input("Enter Flight Number", value=st.session_state.get('cancellation_flight_number', ''), key='cancellation_flight_number')
        st.button("Cancel Booking", on_click=cancel_passenger)

    with st.expander("Check Passenger Status"):
        st.text_input("Enter Passenger ID", value=st.session_state.get('status_passenger_id', ''), key='status_passenger_id')
        st.button("Check Status", on_click=check_passenger_status)

    with st.expander("Check Flight Information"):
        st.text_input("Enter Flight Number", value=st.session_state.get('flight_number', ''), key='flight_number')
        st.button("Check Flight Info", on_click=check_flight_info)


if __name__ == "__main__":
    main()

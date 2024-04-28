
import streamlit as st
from booking_manager import setup_flights_and_seats, handle_waitlist
from cl.flights import Flight
from cl.passengers import Passenger
from cl.waitlist import Waitlist
from utulities.file_reader import read_flights_from_csv, read_passengers_from_csv
from sceduling.searchers import FlightHashTable, PassengerBST
from sceduling.sorters import quick_sort, radix_sort

# Initialize the search structures
flights = FlightHashTable()
passengers = PassengerBST()

# Populate the search structures with data from the CSV files
flights_data = read_flights_from_csv('/scr/data/updated_flights_data.csv')
passengers_data = read_passengers_from_csv('/scr/data/updated_passengers_data_with_new.csv')

for flight in flights_data:
    flights.insert(Flight(flight_number=flight.flight_number,
                          departure_airport=flight.departure_airport, 
                          arrival_airport=flight.arrival_airport, 
                          departure_date=flight.departure_date))

for passenger_data in passengers_data:
    passengers.insert(Passenger(passenger_id=passenger_data.passenger_id,
                                name=passenger_data.name,
                                booking_status=passenger_data.booking_status,
                                seat_number=passenger_data.seat_number,
                                flight_number=passenger_data.flight_number))
# Sort flights by flight number using quick sort
sorted_flights = quick_sort(flights_data, key=lambda flight: flight.flight_number)
# Sort passengers by passenger id using radix sort
sorted_passengers = radix_sort(passengers_data, get_attribute=lambda passenger: passenger.passenger_id)

# Setup flights and seats
setup_flights_and_seats(sorted_flights)

# Function to book a flight
def book_flight(flight_number, passenger_name, seat_class):
    # Check if the flight number is valid
    flight = flights.search_by_flight_number(flight_number)
    if not flight:
        st.error("Invalid flight number")
        return
    
    # Check if the seat class is valid
    if seat_class not in ['First', 'Business', 'Economy']:
        st.error("Invalid seat class")
        return
    
    # Check if the passenger name is provided
    if not passenger_name:
        st.error("Passenger name is required")
        return
    
    if not flight.is_full():    
        # Check if the passenger is already booked on the same flight
        passenger = next((p for p in passengers if p.name == passenger_name), None)

        if passenger is not None:

            if passenger.is_booked(flight_number):
                st.warning("You are already booked on this flight")
                return
        
        # Check if there is an available seat in the requested class
        seat = next((s for s in flight.seats if s.class_type == seat_class), None)
        if not seat.is_available(flight_number):
            st.warning(f"No available {seat_class} seat on this flight")
            return
        
        # Book the seat for the passenger
        seat.book(flight_number, passenger_name)
        
        # Update the flight's passenger count
        flight.increment_passenger_count()
        
        # Handle the waitlist if necessary
        waitlist = Waitlist()
        handle_waitlist(waitlist, flight_number)
        st.success(f"Booked {seat_class} seat for {passenger_name} on flight {flight_number}")
    else:
        st.warning("Sorry, the flight is fully booked")
    if not seat.is_available(flight_number):
        st.warning(f"No available {seat_class} seat on this flight")
        return
    
    # Book the seat for the passenger
    seat.book(flight_number, passenger_name)
    
    # Update the flight's passenger count
    flight.increment_passenger_count()
    
    # Handle the waitlist if necessary
    waitlist = Waitlist()
    handle_waitlist(waitlist, flight_number)
    st.success(f"Booked {seat_class} seat for {passenger_name} on flight {flight_number}")

def cancel_flight(flight_number, passenger_id):
    # Find the flight
    flight = flights.search_by_flight_number(flight_number)
    if not flight:
        st.error(f"Flight {flight_number} not found.")
        return

    # Find the passenger in the flight's passengers list
    passenger = passengers.search(passenger_id)
    if not passenger:
        st.error(f"Passenger {passenger_id} not found on flight {flight_number}.")
        return

    # Remove the passenger from the flight's passengers list
    flight.passengers.remove(passenger)

    # If the passenger is in the flight's waitlist, remove them from there as well
    if passenger in flight.waitlist:
        flight.waitlist.remove_from_waitlist(passenger)

    st.success(f"Booking for passenger {passenger_id} on flight {flight_number} has been cancelled.")

def check_passenger_status(passenger_id):
    # Iterate over all flights
    for flight in flights.get_all_flights():
        # Find the passenger in the flight's passengers list
        passenger = passengers.search(passenger_id)
        if passenger:
            return f"Passenger {passenger_id} is booked on flight {flight.flight_number}, Seat Number: {passenger.seat_number}."
        
        # Check if the passenger is in the flight's waitlist
        if flight.waitlist.is_on_waitlist(passenger_id):  # Pass the passenger_id
            return f"Passenger {passenger_id} is on the waitlist for flight {flight.flight_number}."

    # If the passenger is not found in any flights or waitlists
    return f"Passenger {passenger_id} is not booked on any flights."

def display_passenger_information():
    # Sort passengers by name
    for passenger in sorted_passengers:
        st.write(passenger)

def display_flight_information():
    # Sort flights by flight number
    for flight in sorted_flights:
        st.write(flight)

def display_all_waitlisted_passengers(flight):
    # Iterate over all flights
    for flight in flights.get_all_flights():
        st.write(f"Flight {flight.flight_number} Waitlist:")
        
        for passenger in sorted_passengers:
            if flight.waitlist.is_on_waitlist(passenger):
                st.write(passenger)

# Title of the application
st.title('Flight Booking System')

# Sidebar for navigation
option = st.sidebar.selectbox('Choose an option', ('Booking a Flight', 'Cancelling a Flight', 'Check Passenger Status', 'Flight Information'))

if option == 'Booking a Flight':
    st.header('Book a Flight')
    # Form to book a flight
    with st.form('BookFlight'):
        selected_flight_number = st.selectbox('Select Flight', options=[f.flight_number for f in flights.get_all_flights()], format_func=lambda x: f"Flight {x}")
        selected_flight = flights.search_by_flight_number(selected_flight_number)
        passenger_name = st.text_input('Passenger Name')
        seat_class = st.selectbox('Class', ['First', 'Business', 'Economy'])
        submit_button = st.form_submit_button('Book Flight')
        
        if submit_button:
            book_flight(selected_flight, passenger_name, seat_class)

elif option == 'Cancelling a Flight':
    st.header('Cancel a Flight')
    with st.form('CancelFlight'):
        selected_flight_number = st.selectbox('Select Flight', options=[f.flight_number for f in flights.get_all_flights()], format_func=lambda x: f"Flight {x}")
        selected_flight = flights.search_by_flight_number(selected_flight_number)        
        passenger_id = st.text_input('Passenger ID')
        submit_button = st.form_submit_button('Cancel Booking')
        
        if submit_button:
            cancel_flight(selected_flight, passenger_id)
            st.success(f"Booking for passenger {passenger_id} on flight {selected_flight} has been cancelled.")


elif option == 'Check Passenger Status':
    st.header('Check Passenger Status')
    with st.form('PassengerStatus'):
        passenger_id = st.text_input('Enter Passenger ID')
        check_status_button = st.form_submit_button('Check Status')
        
        if check_status_button:
            status = check_passenger_status(passenger_id)
            st.info(f"Status for passenger ID {passenger_id}: {status}")


elif option == 'Flight Information':
    st.header('Flight Information')
    selected_flight_number = st.selectbox('Select Flight', options=[f.flight_number for f in flights.get_all_flights()], format_func=lambda x: f"Flight {x}")
    selected_flight = flights.search_by_flight_number(selected_flight_number)       
    if st.button('Show Flight Details'):
        if selected_flight:
            for flight in selected_flight:
                flight_info = f"Departure: {flight.departure_airport}, Arrival: {flight.arrival_airport}, Date: {flight.departure_date}  Waitlist: {display_all_waitlisted_passengers(flight.waitlist)}"
                st.write(f"Details for flight {flight.flight_number}: {flight_info}")
        else:
            st.error("No flights found.")


def main():
    # Main function to launch the application
    if __name__ == '__main__':
        st.run(main)


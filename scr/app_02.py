from streamlit import st

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


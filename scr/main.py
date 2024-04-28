from utulities.file_reader import read_flights_from_csv, read_passengers_from_csv
import streamlit as st
from sceduling.searchers import FlightHashTable, PassengerBST

def main():
    # Load data
    flights = read_flights_from_csv('/scr/data/updated_flights_data.csv')
    passengers = read_passengers_from_csv('/scr/data/updated_passengers_data_with_new.csv')

    # Create data structures
    flight_table = FlightHashTable()
    for flight in flights:
        flight_table.insert(flight)

    passenger_tree = PassengerBST()
    for passenger in passengers:
        passenger_tree.insert(passenger)

    # Streamlit app
    st.title('Airline Management System')

    option = st.sidebar.selectbox(
        'Select an option',
        ('Schedule Passenger', 'Cancel Booking', 'Check Passenger Status', 'Display Flight Information')
    )

    if option == 'Schedule Passenger':
        passenger_id = st.text_input('Enter passenger ID')
        flight_number = st.text_input('Enter flight number')
        if st.button('Schedule'):
            # Implement scheduling logic here
            st.success('Passenger scheduled')

    elif option == 'Cancel Booking':
        passenger_id = st.text_input('Enter passenger ID')
        flight_number = st.text_input('Enter flight number')
        if st.button('Cancel'):
            # Implement cancellation logic here
            st.success('Booking cancelled')

    elif option == 'Check Passenger Status':
        passenger_id = st.text_input('Enter passenger ID')
        if st.button('Check Status'):
            # Implement status checking logic here
            st.success('Status checked')

    elif option == 'Display Flight Information':
        flight_number = st.text_input('Enter flight number')
        if st.button('Display Information'):
            # Implement flight information display logic here
            st.success('Flight information displayed')

if __name__ == "__main__":
    main()

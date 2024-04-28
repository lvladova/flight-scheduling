import streamlit as st
from booking_manager_02 import BookingManager

st.title("Flight Booking System")

# Initialize the booking manager
manager = BookingManager()

# Sidebar for flight and passenger data input
with st.sidebar:
    st.header("Flight and Passenger Data")
    flights_csv = st.text_input("Enter path or URL of Flights CSV")
    passengers_csv = st.text_input("Enter path or URL of Passengers CSV")
    if st.button('Load Data'):
        manager.load_data(flights_csv, passengers_csv)
        st.success('Data loaded successfully!')

# Booking Section
st.header("Book a Flight")
with st.form("book_form"):
    flight_number = st.text_input("Flight Number", key="book_flight_number")
    passenger_id = st.text_input("Passenger ID", key="book_passenger_id")
    seat_class = st.selectbox("Class", ["First", "Business", "Economy"], key="book_class")
    book_button = st.form_submit_button("Book Passenger")

if book_button:
    result = manager.book_passenger(flight_number, passenger_id, seat_class)
    st.success(result)

# Cancellation Section
st.header("Cancel a Booking")
with st.form("cancel_form"):
    cancel_flight_number = st.text_input("Flight Number", key="cancel_flight_number")
    cancel_passenger_id = st.text_input("Passenger ID", key="cancel_passenger_id")
    cancel_button = st.form_submit_button("Cancel Booking")

if cancel_button:
    result = manager.cancel_booking(cancel_flight_number, cancel_passenger_id)
    st.success(result)

# Flight Information Section
st.header("Flight Information")
with st.expander("View Flight Details"):
    info_flight_number = st.text_input("Enter Flight Number", key="info_flight_number")
    if st.button("Get Flight Info", key="get_info"):
        info = manager.get_flight_info(info_flight_number)
        st.text(info)

# Passenger Status Section
st.header("Check Passenger Status")
with st.expander("View Passenger Status"):
    status_passenger_id = st.text_input("Enter Passenger ID", key="status_passenger_id")
    if st.button("Check Status", key="check_status"):
        status = manager.get_passenger_status(status_passenger_id)
        st.text(status)

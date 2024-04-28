import csv
from classes.flights import Flight
from classes.passengers import Passenger
import pandas as pd
import requests
from io import StringIO


def read_flights_from_csv(file_path):
    flights = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k.strip(): v for k, v in row.items()}
            flights.append(Flight(row['flight_number'], row['departure_airport'], row['arrival_airport'], row['departure_date']))
    return flights

def read_passengers_from_csv(file_path):
    passengers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            passengers.append(Passenger(row['passenger_id'], row['name'], row['booking_status'], row['seat_number'], row['flight_number']))
    return passengers

def read_csv(file_path):
    """Reads a CSV file from a local path or a URL into a pandas DataFrame."""
    try:
        if file_path.startswith('http://') or file_path.startswith('https://'):
            response = requests.get(file_path)
            response.raise_for_status()  # Ensure that the request was successful
            data = StringIO(response.text)
            df = pd.read_csv(data)
        else:
            df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise IOError(f"Error reading {file_path}: {str(e)}")



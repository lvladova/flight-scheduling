# Flight Scheduling System

## Description
The Flight Scheduling System is designed to manage and operate flight bookings, including scheduling, passenger management, and waitlisting. It supports various operations such as scheduling a passenger for a flight, canceling a booking, and querying flight and passenger status.

## System Structure
flight-scheduling-system/
│
├── data/
│ ├── flights.csv
│ ├── passengers.csv
│ └── waitlist.csv
│
├── src/
│ ├── main.py
│ ├── flight.py
│ ├── passenger.py
│ ├── waitlist.py
│ ├── seat.py
│ ├── scheduling/
│ │ ├── sorter.py
│ │ └── searcher.py
│ └── utilities/
│ ├── file_reader.py
│ └── data_validator.py
│
├── tests/
│ ├── test_flight.py
│ ├── test_passenger.py
│ ├── test_waitlist.py
│ └── test_sort_search.p
│
├── requirements.txt
└── README.md
## Features
- Schedule flights and manage bookings
- Assign seats to passengers based on class availability
- Handle waitlisting for full flights
- Search for flights and passenger details
- Cancel bookings and automatically update waitlisted passengers

## Getting Started

### Prerequisites
- Python 3.8 or above

### Installation
Clone the repository to your local machine:

git clone https://github.com/yourusername/flight-scheduling-system.git


Navigate to the cloned directory:

cd flight-scheduling-system


Install the required dependencies:

pip install -r requirements.txt


### Usage
Run the system with:

python src/main.py


## Testing
To run the tests, use the following command from the root directory:

python -m unittest discover tests



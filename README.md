# Flight Scheduling System

## Description
The Flight Scheduling System is designed to manage and operate flight bookings, including scheduling, passenger management, and waitlisting. It supports various operations such as scheduling a passenger for a flight, canceling a booking, and querying flight and passenger status. 

## System Structure
flight-scheduling

📁 flight-scheduling
│
├── 📁 src                  # Source files
│   ├── 📄 app_04.py           # Main application file
│   ├── 📄 booking_manager_03.py    # Configuration settings for the app
│   ├── 📁 data                 # Data files
│       └── 📄 flights_pile.py       # storing flight data
│       └── 📄 passenger_data.py       # storing passengers data
│   ├── 📁 cl                 # class files 
│       └── 📄 graph.py       # graph structure
│   ├── 📁 sceduling                 # Algorithms
│       └── 📄 searchers.py       # Searchering algorithms
│       └── 📄 sorters.py       # Sorting algorithms
└── 📄 requirements.txt     # Project dependencies
│
└── 📄 README.md     # readme file
│
└── 📄 requirements.txt     # Project dependencies
│
└── 📄 .gitignore    


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

stremlit run dir/app_04.py





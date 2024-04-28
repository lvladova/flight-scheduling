from waitlist import Waitlist as waitlist
from scr.data.flights_pile import flights as flights


class Flight:
    def __init__(self, flight_number, departure_airport, arrival_airport, departure_date):
        self.flight_number = int(flight_number)
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_date = departure_date        
        self.seats = []  # This will hold Seat objects
        self.passengers = []  # This will reference a Passenger object
        self.passenger_count = 0
        self.waitlist = waitlist  # This will reference a Waitlist object
        self.waitlists = {'First': [], 'Business': [], 'Economy': []}  # Waitlists for each class
        self.flights = flights()  # This will reference a Pile object



    def add_passenger(self, passenger, seat_number):
        """Adds a passenger to the flight, ensuring no duplicates."""
        if passenger not in self.passengers:
            seat = next((s for s in self.seats if s.seat_number == seat_number), None)
            if seat and not seat.is_occupied:
                self.passengers.append(passenger)
                passenger.book_flight(self.flight_number, seat)  # Update passenger details
                return True
        return False

    def book_seat(self, passenger, seat_number):
        seat = next((s for s in self.seats if s.seat_number == seat_number), None)
        if seat and not seat.is_occupied:
            seat.assign_passenger(passenger)
        else:
            return "Seat not available or already booked"

    def cancel_seat(self, seat_number):
        seat = next((s for s in self.seats if s.seat_number == seat_number), None)
        if seat and seat.is_occupied:
            seat.remove_passenger()
            # If there are passengers on the waitlist, assign the seat to the next passenger
            if not self.waitlist.is_empty():
                next_passenger = self.waitlist.remove_from_waitlist()
                seat.assign_passenger(next_passenger)

    def remove(self, passenger_id):
        passenger = next((p for p in self.passengers if p.passenger_id == passenger_id), None)
        if passenger:
            self.passenger.remove(passenger)
            # If the passenger is in the flight's waitlist, remove them from there as well
            if self.waitlist.is_on_waitlist(passenger):
                self.waitlist.remove_from_waitlist(passenger)

    def is_full(self):
        return all(seat.is_occupied for seat in self.seats)
    
    def get_flight_info(self):
        return {
            'flight_number': self.flight_number,
            'departure': self.departure_airport,
            'arrival': self.arrival_airport,
            'date': self.departure_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
    
    def increment_passenger_count(self):
        self.passenger_count += 1
        return self.passenger_count

    def schedule_passenger(self, passenger, seat_class):
        """Schedule a passenger on a flight or add to waitlist if full."""
        available_seat = next((seat for seat in self.seats[seat_class] if not seat.is_occupied), None)
        if available_seat:
            available_seat.assign_passenger(passenger)
            return "Passenger booked successfully."
        else:
            self.waitlists[seat_class].append(passenger)
            return "All seats full, added to waitlist."

    def cancel_passenger(self, passenger):
        """Cancel a passenger's booking and handle waitlist."""
        for seat_class, seats in self.seats.items():
            for seat in seats:
                if seat.passenger == passenger:
                    seat.passenger = None
                    if self.waitlists[seat_class]:
                        next_passenger = self.waitlists[seat_class].pop(0)
                        seat.assign_passenger(next_passenger)
                        return f"Passenger {passenger.name} cancelled, {next_passenger.name} has been scheduled."
        return "Passenger not found."

    def get_flight_info(self):
        """Get detailed information about the flight."""
        info = f"Flight {self.flight_number} from {self.departure_airport} to {self.arrival_airport} on {self.departure_date}\n"
        for seat_class, seats in self.seats.items():
            info += f"{seat_class} Seats:\n"
            for seat in seats:
                passenger_name = seat.passenger.name if seat.passenger else "Empty"
                info += f"  Seat {seat.seat_number}: {passenger_name}\n"
        return info

    

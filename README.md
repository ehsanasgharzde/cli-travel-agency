# CLI Travel Agency

This is a Command Line Interface (CLI) travel agency program implemented in Python. It allows users to perform various actions related to airline bookings and travel management.

## Usage

To run the program, execute the `main.py` script.

## Available Commands

### User Authentication

- **Signup:** Create a new user account.
  - Command: `POST signup username password`

- **Login:** Log in to an existing user account.
  - Command: `POST login username password`

- **Logout:** Log out from the current user account.
  - Command: `POST logout`

### User Wallet

- **Check Wallet Balance:** View the current balance in the user's wallet.
  - Command: `GET wallet`

- **Add Funds to Wallet:** Add funds to the user's wallet.
  - Command: `POST wallet amount`

### Flight Information

- **View Available Flights:** List available flights based on optional filters.
  - Command: `GET flights [filters]`
  - Available filters include `from`, `to`, `min_price`, `max_price`, `departure_date`, `min_departure_time`, and `max_departure_time`.

### Flight Booking

- **Book a Flight:** Reserve seats on a flight.
  - Command: `POST tickets flight quantity class type`

- **View Booked Tickets:** List booked tickets for the current user.
  - Command: `GET tickets [ticket_id]`
  - Use `GET tickets` to list all tickets or provide a `ticket_id` to view a specific ticket.

- **Cancel a Ticket:** Cancel a booked ticket (if refundable).
  - Command: `DELETE tickets ticket_id`

### Flight Connections

- **Find Connecting Flights:** Search for connecting flights between two locations.
  - Command: `GET connecting_flights from to`

### Cheapest Flight

- **Find Cheapest Flight:** Find the cheapest direct or connecting flight between two locations.
  - Command: `GET cheapest_flight from to departure_date`

### Reports

- **Generate Overall Report:** View statistical information about flights and users.
  - Command: `GET overall_report`

### Reset

- **Reset Data:** Clear all user data and reset the system.
  - Command: `POST reset`

### Exit

- **Exit Program:** Exit the CLI travel agency program and save data.
  - Command: `POST exit`

## Additional Information

- Valid user authentication (signup and login) is required to access booking and wallet features.
- Some actions may require specific parameters, such as `from`, `to`, `amount`, `quantity`, `class`, `type`, and `ticket_id`. Please provide these as needed.

Enjoy using the CLI Travel Agency for your flight bookings and travel planning!

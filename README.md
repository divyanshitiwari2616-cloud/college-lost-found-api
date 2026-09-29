# College FastAPI Tasks

This repository contains two FastAPI REST API projects developed as part of the college assignment.

---

## Task 1 — College Lost & Found API

A FastAPI-based REST API for reporting and managing lost and found items on campus.

### Technologies

- FastAPI
- SQLModel
- SQLite
- Uvicorn

### Features

- Create lost/found item reports
- View all reported items
- View an item by ID
- Update item details and status
- Delete an item report
- Filter items by status
- Filter items by category
- Input validation
- HTTP error handling

### APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/items` | Create item |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get item by ID |
| PUT | `/items/{item_id}` | Update item |
| DELETE | `/items/{item_id}` | Delete item |
| GET | `/items/status/{status}` | Filter by status |
| GET | `/items/category/{category}` | Filter by category |

---

## Task 2 — Campus Event Seat Reservation API

A FastAPI-based REST API for managing college events and student seat reservations.

### Technologies

- FastAPI
- SQLModel
- SQLite
- Uvicorn

### Features

- Create events
- View all events
- View an event by ID
- Update event information
- Delete events
- Create student reservations
- View event reservations
- Cancel reservations
- Check event availability
- Prevent reservations when capacity is full
- Prevent reservations for closed events
- Validate student email
- Validate event capacity

### APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/events` | Create event |
| GET | `/events` | Get all events |
| GET | `/events/{event_id}` | Get event |
| PUT | `/events/{event_id}` | Update event |
| DELETE | `/events/{event_id}` | Delete event |
| POST | `/events/{event_id}/reserve` | Create reservation |
| GET | `/events/{event_id}/reservations` | Get reservations |
| DELETE | `/reservations/{reservation_id}` | Cancel reservation |
| GET | `/events/{event_id}/availability` | Check seat availability |

---

## Proof of Work

### Task 1

Screenshots demonstrating:

- Create item
- Get all items
- Get item by ID
- Update item
- Delete item
- Status filtering
- Category filtering
- Validation/error handling

Screenshots are available in:

`Task1_Lost_Found_API/screenshots/`

### Task 2

Screenshots demonstrating:

- Create event
- Get events
- Successful reservation
- Get event reservations
- Event availability
- Reservation cancellation
- Full/closed event reservation rejection

Screenshots are available in:

`Task2_Event_Reservation_API/screenshots/`

---

## Database

Both applications use SQLite with SQLModel.

The database engine is created using `create_engine()`, and the required database tables are created when the application starts.

## Running the Projects

Navigate into the required task folder and install dependencies:

```bash
pip install -r requirements.txt
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import EmailStr
from typing import Optional


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# =========================================================
# EVENT MODEL
# =========================================================

class Event(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    title: str
    venue: str
    capacity: int
    organizer: str
    status: str


# =========================================================
# RESERVATION MODEL
# =========================================================

class Reservation(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    event_id: int
    student_name: str
    roll_number: str
    email: str


# =========================================================
# REQUEST MODELS
# =========================================================

class EventCreate(SQLModel):

    title: str
    venue: str
    capacity: int
    organizer: str
    status: str


class EventUpdate(SQLModel):

    title: str
    venue: str
    capacity: int
    organizer: str
    status: str


class ReservationCreate(SQLModel):

    student_name: str
    roll_number: str
    email: EmailStr


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Campus Event Seat Reservation API",
    description="API for managing campus events and student reservations",
    version="1.0.0"
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

@app.on_event("startup")
def create_tables():

    SQLModel.metadata.create_all(engine)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Campus Event Reservation API is running"
    }


# =========================================================
# EVENT APIs
# =========================================================

# 1. POST /events
@app.post("/events", response_model=Event, status_code=201)
def create_event(event: EventCreate):

    # Validate capacity
    if event.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    # Validate status
    if event.status not in ["Open", "Closed"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Open or Closed"
        )

    # Validate title
    if not event.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Event title must not be empty"
        )

    new_event = Event(
        title=event.title.strip(),
        venue=event.venue,
        capacity=event.capacity,
        organizer=event.organizer,
        status=event.status
    )

    with Session(engine) as session:

        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return new_event


# 2. GET /events
@app.get("/events", response_model=list[Event])
def get_events():

    with Session(engine) as session:

        events = session.exec(
            select(Event)
        ).all()

        return events


# 3. GET /events/{event_id}
@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        return event


# 4. PUT /events/{event_id}
@app.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event_data: EventUpdate
):

    if event_data.capacity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    if event_data.status not in ["Open", "Closed"]:

        raise HTTPException(
            status_code=400,
            detail="Status must be Open or Closed"
        )

    if not event_data.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Event title must not be empty"
        )

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        # Don't allow capacity to become smaller
        # than the number of existing reservations
        reservation_statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(
            reservation_statement
        ).all()

        booked = len(reservations)

        if event_data.capacity < booked:

            raise HTTPException(
                status_code=400,
                detail=f"Capacity cannot be less than current bookings ({booked})"
            )

        event.title = event_data.title.strip()
        event.venue = event_data.venue
        event.capacity = event_data.capacity
        event.organizer = event_data.organizer
        event.status = event_data.status

        session.add(event)
        session.commit()
        session.refresh(event)

        return event


# 5. DELETE /events/{event_id}
@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        # Delete reservations belonging to event
        reservation_statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(
            reservation_statement
        ).all()

        for reservation in reservations:
            session.delete(reservation)

        session.delete(event)

        session.commit()

        return {
            "message": "Event deleted successfully"
        }


# =========================================================
# RESERVATION APIs
# =========================================================

# 6. POST /events/{event_id}/reserve
@app.post(
    "/events/{event_id}/reserve",
    status_code=201
)
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate
):

    # Validate student name
    if not reservation_data.student_name.strip():

        raise HTTPException(
            status_code=400,
            detail="Student name must not be empty"
        )

    # Validate email
    if "@" not in reservation_data.email:

        raise HTTPException(
            status_code=400,
            detail="Invalid email address"
        )

    with Session(engine) as session:

        # Check event
        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        # Check event status
        if event.status != "Open":

            raise HTTPException(
                status_code=400,
                detail="Reservations are closed for this event"
            )

        # Count reservations
        reservation_statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(
            reservation_statement
        ).all()

        booked = len(reservations)

        # Check capacity
        if booked >= event.capacity:

            raise HTTPException(
                status_code=400,
                detail="Event is full. No seats available."
            )

        # Create reservation
        reservation = Reservation(
            event_id=event_id,
            student_name=reservation_data.student_name.strip(),
            roll_number=reservation_data.roll_number,
            email=str(reservation_data.email)
        )

        session.add(reservation)

        session.commit()

        session.refresh(reservation)

        return {
            "message": "Reservation created successfully",
            "reservation": reservation
        }


# 7. GET /events/{event_id}/reservations
@app.get("/events/{event_id}/reservations")
def get_reservations(event_id: int):

    with Session(engine) as session:

        # Check event
        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(
            statement
        ).all()

        return reservations


# 8. DELETE /reservations/{reservation_id}
@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):

    with Session(engine) as session:

        reservation = session.get(
            Reservation,
            reservation_id
        )

        if reservation is None:

            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        session.delete(reservation)

        session.commit()

        return {
            "message": "Reservation cancelled successfully"
        }


# 9. GET /events/{event_id}/availability
@app.get("/events/{event_id}/availability")
def get_availability(event_id: int):

    with Session(engine) as session:

        event = session.get(Event, event_id)

        if event is None:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        reservations = session.exec(
            statement
        ).all()

        booked = len(reservations)

        remaining = event.capacity - booked

        return {
            "event_id": event.id,
            "capacity": event.capacity,
            "booked": booked,
            "remaining": remaining
        }
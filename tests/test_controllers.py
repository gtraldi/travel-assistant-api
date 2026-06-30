import pytest
import uuid
from datetime import datetime
from src.models.settings.db_connection_handler import db_connection_handler
from src.models.repositories.trips_repository import TripsRepository
from src.models.repositories.emails_to_invite_repository import EmailsToInviteRepository
from src.models.repositories.activities_repository import ActivitiesRepository
from src.controllers.trip_creator import TripCreator
from src.controllers.trip_finder import TripFinder
from src.controllers.activity_creator import ActivityCreator

# Connect to database and ensure schema is initialized
db_connection_handler.connect()
conn = db_connection_handler.get_connection()

def test_trip_creator_invalid_email():
    trips_repo = TripsRepository(conn)
    emails_repo = EmailsToInviteRepository(conn)
    creator = TripCreator(trips_repo, emails_repo)
    
    # Test invalid owner email
    body = {
        "destination": "London",
        "start_date": "2026-07-10",
        "end_date": "2026-07-20",
        "owner_name": "John Doe",
        "owner_email": "invalid_email_format"
    }
    response = creator.create(body)
    assert response["status_code"] == 400
    assert "Invalid owner_email" in response["body"]["message"]

def test_trip_creator_invalid_date_range():
    trips_repo = TripsRepository(conn)
    emails_repo = EmailsToInviteRepository(conn)
    creator = TripCreator(trips_repo, emails_repo)
    
    # Test end_date before start_date
    body = {
        "destination": "London",
        "start_date": "2026-07-20",
        "end_date": "2026-07-10",
        "owner_name": "John Doe",
        "owner_email": "john.doe@example.com"
    }
    response = creator.create(body)
    assert response["status_code"] == 400
    assert "end_date cannot be before start_date" in response["body"]["message"]

def test_trip_finder_not_found():
    trips_repo = TripsRepository(conn)
    finder = TripFinder(trips_repo)
    
    # Test non-existent trip id returns 404
    non_existent_id = str(uuid.uuid4())
    response = finder.find_trip_details(non_existent_id)
    assert response["status_code"] == 404
    assert response["body"]["error"] == "Not Found"

def test_activity_creator_out_of_range():
    trips_repo = TripsRepository(conn)
    activities_repo = ActivitiesRepository(conn)
    creator = ActivityCreator(activities_repo, trips_repo)
    
    # 1. Create a trip first to get a valid trip_id
    emails_repo = EmailsToInviteRepository(conn)
    trip_creator = TripCreator(trips_repo, emails_repo)
    trip_id = str(uuid.uuid4())
    
    # Insert trip details directly
    trip_infos = {
        "id": trip_id,
        "destination": "London",
        "start_date": "2026-07-10",
        "end_date": "2026-07-20",
        "owner_name": "John Doe",
        "owner_email": "john@example.com"
    }
    trips_repo.create_trip(trip_infos)
    
    # Test activity occurs before start_date
    body_before = {
        "title": "Museum visit",
        "occurs_at": "2026-07-09 10:00:00"
    }
    response_before = creator.create(body_before, trip_id)
    assert response_before["status_code"] == 400
    assert "must be within trip range" in response_before["body"]["message"]
    
    # Test activity occurs after end_date
    body_after = {
        "title": "Museum visit",
        "occurs_at": "2026-07-21 10:00:00"
    }
    response_after = creator.create(body_after, trip_id)
    assert response_after["status_code"] == 400
    assert "must be within trip range" in response_after["body"]["message"]
    
    # Test activity occurs within range (success)
    body_valid = {
        "title": "Museum visit",
        "occurs_at": "2026-07-15 10:00:00"
    }
    response_valid = creator.create(body_valid, trip_id)
    assert response_valid["status_code"] == 201

import pytest
import uuid
from src.models.settings.db_connection_handler import db_connection_handler
from .activities_repository import ActivitiesRepository

db_connection_handler.connect()
trip_id = str(uuid.uuid4())


@pytest.mark.skip(reason="interacao com o banco")
def test_registry_email():
    conn = db_connection_handler.get_connection()
    activities_repository = ActivitiesRepository(conn)

    activity_infos = {
        "id": str(uuid.uuid4()),
        "trip_id": trip_id,
        "title": "Titulo Teste",
        "occurs_at": "22-09-2024"
    }

    activities_repository.registry_activity(activity_infos)


@pytest.mark.skip(reason="interacao com o banco")
def test_find_activity_from_trip():
    conn = db_connection_handler.get_connection()
    activities_repository = ActivitiesRepository(conn)

    activity = activities_repository.find_activity_from_trip(trip_id)
    
import pytest
import uuid
from .participants_repository import PaticipantsRepository
from src.models.settings.db_connection_handler import db_connection_handler


db_connection_handler.connect()

participant_id = str(uuid.uuid4())
trip_id = "testeId"

@pytest.mark.skip(reason="interacao com o banco")
def test_registry_participant():
    conn = db_connection_handler.get_connection()
    participant_repository = PaticipantsRepository(conn)

    participant_infos = {
        "id": participant_id,
        "trip_id": trip_id,
        "emails_to_invite_id": "idTeste",
        "name": "Ronaldo"
    }

    participant_repository.registry_participant(participant_infos)


@pytest.mark.skip(reason="interacao com o banco")
def test_find_participants_from_trip():
    conn = db_connection_handler.get_connection()
    participant_repository = PaticipantsRepository(conn)

    participants = participant_repository.find_participants_from_trip(trip_id)
    assert isinstance(participants, list)
    assert isinstance(participants[0], tuple)


@pytest.mark.skip(reason="interacao com o banco")
def test_update_participant_status():
    conn = db_connection_handler.get_connection()
    participant_repository = PaticipantsRepository(conn)

    participant_repository.update_participant_status(participant_id)

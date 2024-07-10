import pytest
import uuid
from .links_repository import LinksRepository
from src.models.settings.db_connection_handler import db_connection_handler


db_connection_handler.connect()

link_id = str(uuid.uuid4())
trip_id = str(uuid.uuid4())


@pytest.mark.skip(reason="interacao com o banco")
def test_registry_email():
    conn = db_connection_handler.get_connection()
    links_reposoitory = LinksRepository(conn)

    link_infos = {
        "id": link_id,
        "trip_id": trip_id,
        "link": "linkteste.com",
        "title": "Hotel"
    }

    links_reposoitory.registry_link(link_infos)


@pytest.mark.skip(reason="interacao com o banco")
def test_find_link_from_trip():
    conn = db_connection_handler.get_connection()
    link_repository = LinksRepository(conn)

    links = link_repository.find_links_from_trip(trip_id)
    assert isinstance(links, list)
    assert isinstance(links[0], tuple)
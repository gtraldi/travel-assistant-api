import uuid
from typing import Dict


class LinkCreator:
    def __init__(self, link_repository) -> None:
        self.__link_repository = link_repository

    
    def create(self, body, trip_id) -> Dict:
        try:
            if not body or not isinstance(body, dict):
                return {
                    "body": {"error": "Bad Request", "message": "Invalid request body"},
                    "status_code": 400
                }

            required_fields = ["url", "title"]
            for field in required_fields:
                if field not in body:
                    return {
                        "body": {"error": "Bad Request", "message": f"Missing required field: '{field}'"},
                        "status_code": 400
                    }

            link_id = str(uuid.uuid4())
            link_infos = {
                "link": body["url"],
                "title": body["title"],
                "id": link_id,
                "trip_id": trip_id
            }

            self.__link_repository.registry_link(link_infos)

            return {
                "body": { "linkId": link_id },
                "status_code": 201
            }
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
        
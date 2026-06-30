import uuid
from typing import Dict

class ParticipantCreator:
    def __init__(self, participants_repository, emails_repository) -> None:
        self.__participants_repository = participants_repository
        self.__emails_repository = emails_repository

    
    def create(self, body, trip_id) -> Dict:
        try:
            if not body or not isinstance(body, dict):
                return {
                    "body": {"error": "Bad Request", "message": "Invalid request body"},
                    "status_code": 400
                }

            required_fields = ["email", "name"]
            for field in required_fields:
                if field not in body:
                    return {
                        "body": {"error": "Bad Request", "message": f"Missing required field: '{field}'"},
                        "status_code": 400
                    }

            participant_id = str(uuid.uuid4())
            email_id = str(uuid.uuid4())

            emails_infos = {
                "email": body["email"],
                "id": email_id,
                "trip_id": trip_id
            }

            participant_infos = {
                "id": participant_id,
                "trip_id": trip_id,
                "emails_to_invite_id": email_id,
                "name": body["name"]
            }

            self.__emails_repository.registry_email(emails_infos)
            self.__participants_repository.registry_participant(participant_infos)

            return {
                "body": { "participant_id": participant_id},
                "status_code": 201
            }
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
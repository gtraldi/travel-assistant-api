import uuid
from typing import Dict

from src.drivers.email_sender import send_email
from src.utils.validators import is_valid_email, parse_date


class TripCreator:
    def __init__(self, trip_repository, emails_repository) -> None:
        self.__trip_repository = trip_repository
        self.__emails_repository = emails_repository

    
    def create(self, body) -> Dict:
        try:
            if not body or not isinstance(body, dict):
                return {
                    "body": {"error": "Bad Request", "message": "Invalid request body"},
                    "status_code": 400
                }

            required_fields = ["destination", "start_date", "end_date", "owner_name", "owner_email"]
            for field in required_fields:
                if field not in body:
                    return {
                        "body": {"error": "Bad Request", "message": f"Missing required field: '{field}'"},
                        "status_code": 400
                    }

            # Email format validation
            if not is_valid_email(body["owner_email"]):
                return {
                    "body": {"error": "Bad Request", "message": "Invalid owner_email format"},
                    "status_code": 400
                }

            # Date consistency validation
            try:
                start_dt = parse_date(body["start_date"])
                end_dt = parse_date(body["end_date"])
                if end_dt < start_dt:
                    return {
                        "body": {"error": "Bad Request", "message": "end_date cannot be before start_date"},
                        "status_code": 400
                    }
            except ValueError as e:
                return {
                    "body": {"error": "Bad Request", "message": str(e)},
                    "status_code": 400
                }

            emails = body.get("emails_to_invite")
            if emails:
                for email in emails:
                    if not is_valid_email(email):
                        return {
                            "body": {"error": "Bad Request", "message": f"Invalid email format in invites: '{email}'"},
                            "status_code": 400
                        }

            trip_id = str(uuid.uuid4())
            trip_infos = {**body, "id": trip_id}

            self.__trip_repository.create_trip(trip_infos)

            if emails:
                for email in emails:
                    self.__emails_repository.registry_email({
                        "email": email,
                        "trip_id": trip_id,
                        "id": str(uuid.uuid4())
                    })
            
            send_email(
                [body["owner_email"]],
                f"http://localhost:3000/trips/{trip_id}/confirm"
            )

            return {
                "body": {"id": trip_id},
                "status_code": 201
            }
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
        

import uuid
from typing import Dict
from src.utils.validators import parse_date

class ActivityCreator:
    def __init__(self, activities_repository, trips_repository) -> None:
        self.__activities_repository = activities_repository
        self.__trips_repository = trips_repository

    
    def create(self, body, trip_id) -> Dict:
        try:
            if not body or not isinstance(body, dict):
                return {
                    "body": {"error": "Bad Request", "message": "Invalid request body"},
                    "status_code": 400
                }

            required_fields = ["title", "occurs_at"]
            for field in required_fields:
                if field not in body:
                    return {
                        "body": {"error": "Bad Request", "message": f"Missing required field: '{field}'"},
                        "status_code": 400
                    }

            # Business rule validation: activity date must fall within trip range
            trip = self.__trips_repository.find_trip_by_id(trip_id)
            if not trip:
                return {
                    "body": {"error": "Not Found", "message": "Trip not found"},
                    "status_code": 404
                }

            try:
                trip_start = parse_date(trip[2]) # start_date
                trip_end = parse_date(trip[3])   # end_date
                activity_time = parse_date(body["occurs_at"])
                
                if not (trip_start <= activity_time <= trip_end):
                    return {
                        "body": {
                            "error": "Bad Request",
                            "message": f"Activity date '{body['occurs_at']}' must be within trip range '{trip[2]}' to '{trip[3]}'"
                        },
                        "status_code": 400
                    }
            except ValueError as e:
                return {
                    "body": {"error": "Bad Request", "message": str(e)},
                    "status_code": 400
                }

            activity_id = str(uuid.uuid4())
            activities_infos = {
                "id": activity_id,
                "trip_id": trip_id,
                "title": body["title"],
                "occurs_at": body["occurs_at"]
            }

            self.__activities_repository.registry_activity(activities_infos)
            
            return {
                "body": { "activityId": activity_id},
                "status_code": 201
            }
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }

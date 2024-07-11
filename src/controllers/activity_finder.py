from typing import Dict


class ActivityFinder:
    def __init__(self, activity_repository) -> None:
        self.__activity_repository = activity_repository


    def find_activity_from_trip(self, trip_id: str) -> Dict:
        try:
            activities = self.__activity_repository.find_activity_from_trip(trip_id)

            formatted_activities = []
            for activity in activities:
                formatted_activities.append({
                    "id": activity[0],
                    "title": activity[2],
                    "occurs_at": activity[3]
                })

            return {
                "body": { "activity": formatted_activities},
                "status_code": 200
            }
        except Exception as exception:
            return {
                "body": {"error": "Bad Request", "message": str(exception)},
                "status_code": 400
            }
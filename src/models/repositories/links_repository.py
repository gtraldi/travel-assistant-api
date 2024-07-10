from sqlite3 import Connection
from typing import Dict, Tuple, List


class LinksRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def registry_link(self, links_info : Dict) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
                INSERT INTO links
                    (id, trip_id, link, title)
                VALUES
                    (?, ?, ?, ?)
            """ , (
                links_info["id"],
                links_info["trip_id"],
                links_info["link"],
                links_info["title"],
            )
        )

        self.__conn.commit()

    def find_links_from_trip(self, trip_id: str) -> List[Tuple]:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
                SELECT * FROM links WHERE trip_id = ?
            """, (trip_id,)
        )

        links = cursor.fetchall()
        return links

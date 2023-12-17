import datetime
import os

import isodate  # type: ignore

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build  # type: ignore


class PlayList:
    """Класс для получения информации о плейлисте по его id"""

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется по id плейлиста. Дальше все данные будут подтягиваться по API."""

        self.youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

        # id плейлиста
        self.playlist_id = playlist_id

        # Получение информации о плейлисте.
        self.playlist_info = (
            self.youtube.playlists().list(id=self.playlist_id, part="snippet").execute()
        )
        # получение информации по видео в плейлисте.
        self.videos_in_playlist_info = (
            self.youtube.playlistItems()
            .list(
                playlistId=self.playlist_id,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )
        # получение id всех видео из плейлиста
        self.video_ids: list[str] = [
            video["contentDetails"]["videoId"]
            for video in self.videos_in_playlist_info["items"]
        ]
        # название плейлиста
        self.title = self.playlist_info["items"][0]["snippet"]["title"]

        # ссылка на плейлист
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        """Вычисляет общую длительность всех роликов из плейлиста"""

        video_response = (
            self.youtube.videos()
            .list(part="contentDetails,statistics", id=",".join(self.video_ids))
            .execute()
        )
        total_duration = datetime.timedelta()

        for item in video_response["items"]:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = item["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на видео с наибольшим количеством лайков."""
        url_video = ""
        likes = 0
        for item in self.video_ids:
            like_count = self.get_statistic_video(item)
            if like_count > likes:
                url_video = f"https://youtu.be/{item}"
        return url_video

    def get_statistic_video(self, video_id: str) -> int:
        video_info = (
            self.youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=video_id)
            .execute()
        )

        return int(video_info["items"][0]["statistics"]["likeCount"])

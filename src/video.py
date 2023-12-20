import os

from dotenv import load_dotenv
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build  # type: ignore

load_dotenv()

API_YOUTUBE = os.getenv("YOUTUBE_API_KEY")


class Video:
    """Класс для получения информации о видео по его id"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""

        try:
            youtube = build("youtube", "v3", developerKey=API_YOUTUBE)
            self.video_response = (
                youtube.videos()
                .list(
                    part="snippet,statistics,contentDetails,topicDetails", id=video_id
                )
                .execute()
            )
            # id видео
            self.video_id: str = video_id

            # Название видео
            self.title: str | None = self.video_response["items"][0]["snippet"]["title"]

            # Ссылка на видео
            self.url: str | None = f"https://youtu.be/{self.video_id}"

            # Количество просмотров
            self.view_count: int | None = self.video_response["items"][0]["statistics"][
                "viewCount"
            ]

            # Количество лайков
            self.like_count: int | None = self.video_response["items"][0]["statistics"][
                "likeCount"
            ]
        except IndexError:

            # id видео
            self.video_id = video_id

            # Ссылка на видео
            self.url = None

            # Название видео
            self.title = None

            # Количество просмотров
            self.view_count = None

            # Количество лайков
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)

        # id плейлиста
        self.playlist_id = playlist_id

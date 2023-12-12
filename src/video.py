import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        self.video_response = (
            youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=video_id)
            .execute()
        )
        # id видео
        self.video_id = video_id

        # Название видео
        self.video_title: str = self.video_response["items"][0]["snippet"]["title"]

        # Ссылка на видео
        self.url = f"https://youtu.be/gaoc9MPZ4bw{self.video_id}"

        # Количество просмотров
        self.view_count: int = self.video_response["items"][0]["statistics"][
            "viewCount"
        ]

        # Количество лайков
        self.like_count: int = self.video_response["items"][0]["statistics"][
            "likeCount"
        ]

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)

        # id плейлиста
        self.playlist_id = playlist_id

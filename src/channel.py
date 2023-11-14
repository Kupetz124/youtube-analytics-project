import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__api_object = build(
            "youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY")
        )
        self.channel_info = (
            self.__api_object.channels()
            .list(id=channel_id, part="snippet,statistics")
            .execute()
        )
        self.__channel_id: str = channel_id
        self.title: str = self.channel_info["items"][0]["snippet"]["title"]
        self.channel_description: str = self.channel_info["items"][0]["snippet"][
            "description"
        ]
        self.url: str = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count: int = self.channel_info["items"][0]["statistics"][
            "subscriberCount"
        ]
        self.video_count: int = self.channel_info["items"][0]["statistics"][
            "videoCount"
        ]
        self.view_count: int = self.channel_info["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """
        Записывает атрибуты экземпляра в json формате.
        """
        new_dict = self.__dict__.copy()
        new_dict.pop("_Channel__api_object", None)
        new_dict.pop("channel_info", None)

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(new_dict, file, ensure_ascii=False, indent=3)

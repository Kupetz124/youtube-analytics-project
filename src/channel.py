import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build  # type: ignore


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        self.channel_info = (
            self.youtube.channels()
            .list(id=channel_id, part="snippet,statistics")
            .execute()
        )
        # id канала
        self.__channel_id: str = channel_id

        # Название канала
        self.title: str = self.channel_info["items"][0]["snippet"]["title"]

        # Описание канала
        self.channel_description: str = self.channel_info["items"][0]["snippet"][
            "description"
        ]
        # ссылка на канал
        self.url: str = f"https://www.youtube.com/channel/{self.__channel_id}"

        # количество подписчиков канала
        self.subscriber_count: int = self.channel_info["items"][0]["statistics"][
            "subscriberCount"
        ]
        # количество видео на канале
        self.video_count: int = self.channel_info["items"][0]["statistics"][
            "videoCount"
        ]
        # количество просмотров на канале
        self.view_count: int = self.channel_info["items"][0]["statistics"]["viewCount"]

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """Метод для сложения двух экземпляров класса."""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        """Метод для вычитания двух экземпляров класса."""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other) -> bool:
        """Метод для операции сравнения '==' двух экземпляров класса."""
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        """Метод для операции сравнения '>' двух экземпляров класса."""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __lt__(self, other) -> bool:
        """Метод для операции сравнения '<' двух экземпляров класса."""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __ge__(self, other) -> bool:
        """Метод для операции сравнения '>=' двух экземпляров класса."""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __le__(self, other) -> bool:
        """Метод для операции сравнения '<=' двух экземпляров класса."""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    @property
    def channel_id(self) -> str:
        """
        Возвращает значение __channel_id (id канала)
        """
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

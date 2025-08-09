from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class search_write:
    """
    Класс для записи логов поисковых запросов в MongoDB.
    """
    def __init__(self):
        # Подключение к MongoDB через переменные окружения
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.collection = self.db[os.getenv("MONGO_COLLECTION_NAME")]


    def log_search(self, search_type, params, results_count:int):
        """
        Записывает один поисковый запрос в MongoDB, если тип запроса допустим.

        :param search_type: строка, например "by title"
        :param params: словарь с параметрами поиска
        :param results_count: количество результатов, полученных по запросу
        """
        # Допустимые типы поиска
        allowed_search_types = ["by title", "by year", "by genre",
                                "by actor", "by years (from... to...)",
                                "by genre and years"]
        # Если тип поиска не из разрешённых — не логируем
        if search_type not in allowed_search_types:
            return
        # Формируем запись лога
        log_entry={
            "timestamp": datetime.now(),# Время запроса
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }
        # Сохраняем лог в MongoDB
        self.collection.insert_one(log_entry)
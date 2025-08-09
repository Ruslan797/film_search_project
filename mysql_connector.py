import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class DBConnector:
    """
    Класс для подключения и взаимодействия с базой данных MySQL.
    Все методы возвращают результат SQL-запросов.
    """

    def __init__(self):
        # Подключение к базе данных с использованием переменных окружения
        self.connection = pymysql.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            cursorclass=DictCursor,
        )

    def get_genres(self):
        """
        Получить список всех уникальных жанров.
        """
        query = """
                    SELECT DISTINCT name
                    FROM  category 
                """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return [row["name"] for row in cursor.fetchall()]

    def get_years_by_genre(self, genre):
        """
        Получить диапазон годов (мин/макс) релизов по определённому жанру.
        :param genre:
        :return:мин/макс года для жанра
        """
        query = """
                    Select MIN(f.release_year) as year_from, MAX(f.release_year) as year_to
                    from film as f
                    join film_category as fc
                    on f.film_id=fc.film_id
                    join category as c
                    on fc.category_id=c.category_id
                    where c.name=%s

                """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (genre,))
            return cursor.fetchall()

    def search_film_name(self, name, offset=0, limit=10):
        """
        Поиск фильмов по названию. Поддерживает пагинацию через offset и limit.
        :param name:
        :param offset: 0 по дефолту
        :param limit: 10
        :return: наименование фильмов и их год выхода
        """
        with self.connection.cursor() as cursor:
            query = """
                    SELECT title, release_year
                    FROM film
                    Where title like %s
                    LIMIT %s OFFSET %s
                 """
            cursor.execute(query, (f"%{name.lower()}%", limit, offset))
            return cursor.fetchall()

    def search_film_year(self, year):
        """
        Поиск фильмов по конкретному году выпуска.
        :param year:
        :return: наименование фильмов и их год выхода
        """
        query = """
                SELECT title, release_year
                FROM film
                Where release_year = %s;
            """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (year,))
            return cursor.fetchall()

    def search_film_genre(self, genre):
        """
        Поиск фильмов по жанру.
        :param genre:
        :return: наименование фильмов и их год выхода, а также жанр
        """
        query = """
                SELECT f.title, f.release_year, c.name as genre
                FROM film as f
                JOIN film_category as fc
                ON f.film_id=fc.film_id
                JOIN category as c
                ON fc.category_id=c.category_id
                Where c.name like %s;
            """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (f"%{genre}%",))
            return cursor.fetchall()

    def search_film_actor(self, actor_name):
        """
        Поиск фильмов по имени актёра (имя + фамилия).
        :param actor_name:
        :return: наименование фильмов и их год выхода, а также имя актера, по которому выборка
        """
        query = """
                     SELECT f.title, f.release_year, CONCAT(a.first_name," ",a.last_name) as actor_name
                     FROM film as f
                     JOIN film_actor as fa
                     ON f.film_id=fa.film_id
                     JOIN actor as a
                     ON fa.actor_id=a.actor_id
                     Where LOWER(CONCAT(a.first_name," ",a.last_name)) like %s;
                """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (f"%{actor_name}%",))
            return cursor.fetchall()

    def search_film_years(self, year_from, year_to):
        """
        Поиск фильмов в диапазоне годов.
        :param year_from:
        :param year_to:
        :return: наименование фильмов и года введеного диапазона
        """
        query = """
                  SELECT title, release_year
                  FROM film
                  Where release_year BETWEEN %s AND %s;
                """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (year_from, year_to))
            return cursor.fetchall()

    def search_film_genre_and_years(self, genre, year_from, year_to):
        """
        Поиск фильмов по жанру и диапазону годов.
        :param genre:
        :param year_from:
        :param year_to:
        :return: наименование фильмов, жанра и годов введеного диапазона
        """
        query = """
                    SELECT f.title, f.release_year, c.name as genre
                    FROM film as f
                    JOIN film_category as fc
                    ON f.film_id=fc.film_id
                    JOIN category as c
                    ON fc.category_id=c.category_id
                    Where c.name like %s AND f.release_year BETWEEN %s AND %s;
                """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (f"%{genre}%", year_from, year_to))
            return cursor.fetchall()

    def get_genres_with_years(self):
        """
         Получить список жанров с минимальным и максимальным годом релиза для каждого жанра.
        :return: список жанров и имеющихся в каждом жанре годов
        """
        query = """
                    Select distinct c.name as genre, MIN(f.release_year) as year_from, MAX(f.release_year) as year_to
                    from film as f 
                    join film_category as fc
                    on f.film_id=fc.film_id
                    join category as c
                    on c.category_id=fc.category_id
                    group by c.name
                    order by c.name;
                """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        """
         Закрытие соединения с базой данных.
        """
        if self.connection:
            self.connection.close()




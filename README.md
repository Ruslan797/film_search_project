# 🎬 film_search_project

Это консольное Python-приложение для поиска фильмов в базе данных **MySQL** с логированием запросов в **MongoDB** и возможностью просмотра популярных и последних поисков.

---

## 📌 Возможности:

- Поиск фильмов по:
- названию
- году выпуска
- диапазону лет
- жанру
- жанру + годам
- имени актёра
- Постраничный вывод результатов
- Логирование каждого поиска (тип, параметры, количество найденных записей, время)
- Просмотр:
- топ-5 самых популярных запросов
- последних 5 уникальных запросов

- 
⚙️ Установка

1. Клонирование проекта
git clone https://github.com/your-username/Final_project.git
cd film_search_project

3. Установка зависимостей
pip install -r requirements.txt


4. Настройка окружения
  
   
Создайте файл .env в корне проекта и добавьте туда:


MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=your_db
MONGO_COLLECTION_NAME=search_logs
Также убедитесь, что в mysql_connector.py указаны правильные данные для подключения к MySQL.




📁 Структура проєкту

Final_project/
│
├── .env                  # Переменные окружения (не коммитится)
├── .gitignore            # Игнорируемые файлы для Git
├── formatter.py          # Форматированный вывод таблиц и пагинация
├── log_stats.py          # Получение статистики логов из MongoDB
├── log_writer.py         # Запись логов поисков в MongoDB
├── main.py               # Главный файл запуска
├── mysql_connector.py    # Подключение и SQL-запросы к MySQL
├── README.md             # Этот файл
├── requirements.txt      # Зависимости проекта
├── search_def.py         # Реализация поисковых функций


python main.py
🧩 Описание основных файлов
- main.py — точка входа, запускает меню и обрабатывает ввод пользователя.
- search_def.py — содержит функции:
- search_film_name()
- search_film_year()
- search_film_years_range()
- search_film_gerne()
- search_film_gerne_and_years()
- search_film_actor()
- show_popular_searches()
- show_last_searches()
- formatter.py — функции print_table() и paginate_results() для вывода результатов.
- log_writer.py — логирование запросов в MongoDB (тип, параметры, время, количество).
- log_stats.py — функции для получения статистики:
- топ-5 запросов
- последние 5 уникальных запросов
- mysql_connector.py — подключение к MySQL и выполнение запросов.

🛠 Используемые технологии
- Python 3.10+
- MySQL — база данных фильмов
- MongoDB — хранение логов
- Pymongo
- mysql-connector-python
- python-dotenv

---



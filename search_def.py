from mysql_connector import DBConnector
from log_writer import search_write
from log_stats import *
from formatter import (
                        GREEN,
                        MAGENTA,
                        RESET,
                        BERUSA,
                        print_table,
                        paginate_results
                      )

# Инициализация базы данных и логгера
db=DBConnector() # Подключение к базе данных
logger = search_write()   # Объект логгера для записи поисков
statistic=LogStats(logger)  # Объект статистики, использующий логгер



def search_film_name():
    while True:
        # Запрашиваем у пользователя название фильма
        name = input(f"{GREEN}Enter movie title (or 0 to return to main menu): {RESET}").strip()
        if name=="0":
            return # Выход в главное меню
        if  not name:
            print(f"{BERUSA}Can not be empty.{RESET}") # Проверка на пустой ввод
            continue

        # Поиск по названию
        results = db.search_film_name(name)
        if not results:
            print(f"{BERUSA}No films found for title {name.title()}.{RESET}")
            continue

        # Запись поиска в лог
        logger.log_search("by title", {"title": name}, len(results))

        # Вывод результатов с пагинацией
        action=paginate_results(results, ["title", "release_year"])
        if action=="back":# Вернуться к вводу
            continue
        elif action=="menu":# Вернуться в главное меню
            return
        break



def search_film_year():
    """
    Функция для поиска фильмов по году выпуска.
    """
    while True:
        try:
            # Ввод года выпуска
            user_inp = int(input(f"{GREEN}Enter release year(from 1990) or 0 to return to main menu: {RESET}"))
        except ValueError:
            # Если введено не число, сообщаем об ошибке и запрашиваем ввод заново
            print(f"{BERUSA}Invalid year format.{RESET}")
            continue

        if user_inp == 0: # Вернуться в главное меню
            return

        # Проверка на необходимость ввода 1990 и выше, так как это минимальный год
        if user_inp<1990:
            print(f"{BERUSA}Invalid year, must be 1990 or later.{RESET}")
            continue

        # Выполняем поиск фильмов по введённому году
        results = db.search_film_year(user_inp)

        # проверка на наличие результата, если его нет, возвращаемся к вводу года
        if not results:
            print(f"{GREEN}No films found for this year {user_inp}.{RESET}")
            continue
        logger.log_search("by year", {"year":user_inp}, len(results))
        action=paginate_results(results, ["title", "release_year"])
        if action=="back": # Если пользователь выбрал "назад", повторяем запрос года
            continue
        elif action=="menu": # Если пользователь выбрал "меню", возвращаемся в главное меню
            return
        break  # Завершаем функцию после успешного поиска и вывода результатов


def search_film_genre():
    """
    Функция для поиска фильмов по жанру.
    """
    while True:
        # Получаем список жанров из базы данных
        genres=db.get_genres()

        # Выводим жанры в табличном виде с номерами
        print_table([{"#": i+1, "Genre": g} for i, g in enumerate(genres)], ["#","Genre" ])
        try:
            # Запрашиваем у пользователя номер жанра (сделано -1, чтобы получить индекс в списке)
            index_=int(input(f"{GREEN}Choose genre numbeerror: {RESET}"))-1

            # Проверяем, что введённый индекс находится в пределах списка жанров
            if index_ not in range(len(genres)):
                print(f"{BERUSA}Invalid selection.{RESET}")
                return

            # Получаем название выбранного жанра
            genre=genres[index_]

            # Поиск фильмов по выбранному жанру
            results=db.search_film_genre(genre)

            # Логируем поиск в MongoDB
            logger.log_search("by genre", {"genre": genre}, len(results))

            # Выводим результаты с пагинацией
            action=paginate_results(results, ["title", "release_year"])
            if action == "back":  # Если пользователь хочет вернуться — повторяем выбор жанра
                continue
            elif action == "menu":   # Возвращаемся в главное меню
                return
        except ValueError:  # Обработка ошибки, если ввод не является числом
            print(f"{BERUSA}Invalid input.{RESET}")

def search_film_actor():
    """
    Функция для поиска фильмов по имени актёра.
    """
    while True:
        # Запрашиваем имя актёра, переводим в нижний регистр и убираем пробелы по краям
        actor=input(f"{GREEN}Enter actor name(or 0 to return to main menu): {RESET}").strip().lower()

        # Если введено "0" — выходим из функции, возвращаясь в главное меню
        if actor=="0":
            return

        # Проверяем, что имя актёра не пустое
        elif not actor:
            print(f"{BERUSA}Actor name cannot be empty. Try again.{RESET}")
            continue

        # Выполняем поиск фильмов с указанным актёром
        results=db.search_film_actor(actor)

        # Если результатов нет — сообщаем и просим попробовать снова
        if not results:
            print(f"{GREEN}No films found for actor {actor.title()}. Try again.{RESET}")
            continue

        # Логируем поисковый запрос в MongoDB
        logger.log_search("by actor", {"actor": actor.title()}, len(results))

        # Показываем результаты с пагинацией, отображая название, год и имя актёра
        action=paginate_results(results, ["title", "release_year", "actor_name"])
        if action=="back":  # Если пользователь выбрал "назад" — повторяем цикл для нового ввода
            continue
        elif action=="menu":  # Если выбрал "меню" — выходим из функции
            return
        break  # Если всё успешно, выходим из цикла (и функции)

def search_film_years_range():
    """
    Функция для поиска фильмов по диапазону годов выпуска.
    """
    while True:
        try:
            # Запрашиваем год начала диапазона
            year_from= int(input(f"{GREEN}From year: {RESET}"))
            # Запрашиваем год конца диапазона
            year_to=int(input(f"{GREEN}To year: {RESET}"))

            # Проверяем, что годы не меньше 1990
            if year_from<1990 or year_to<1990:
                print(f"{BERUSA}Invalid year, must be 1990 and greate.{RESET}")
                continue

            # Проверяем, что год начала не больше года конца
            elif year_from > year_to:
                print(f"{BERUSA}Error: 'From year' cannot be greater than 'To year'.{RESET}")
                continue

        except ValueError:
            # Обработка ошибки, если введено не число
            print(f"{BERUSA}Invalid year format.{RESET}")
            return

        # Выполняем поиск фильмов по указанному диапазону годов
        results=db.search_film_years(year_from,year_to)

        # Логируем поисковый запрос в MongoDB
        logger.log_search("by years (from... to...)", {"from":year_from,"to":year_to}, len(results))

        # Выводим результаты с пагинацией (показываем поля title и release_year)
        action=paginate_results(results, ["title", "release_year"])

        if action=="back":# Если пользователь выбрал "назад" — повторяем цикл для нового ввода
            continue
        elif action=="menu":# Если выбрал "меню" — выходим из функции
            return

def search_film_genre_and_years():
    """
    Функция для поиска фильмов по выбранному жанру и диапазону лет.
    """
    while True:
        # Получаем список жанров с диапазоном доступных лет
        genres = db.get_genres_with_years()

        # Выводим таблицу жанров с их диапазонами годов
        print("\t Genre   \t|  Years")
        print("-"*84)
        for i, genre in enumerate(genres,1):
            print(f"{i:2} | {genre['genre']:<11} | {genre['year_from']} - {genre['year_to']}")
        try:
            # Запрашиваем выбор жанра по номеру
            index_=int(input(f"{GREEN}Choice genre number(or 0 to return to main menu): {RESET}"))-1
            if index_ == "0":  # 0 - вернуться в меню
                return
            elif  not (0<=index_<len(genres)):
                print(f"{BERUSA}Invalid genre selection.{RESET}")
                return

            # Получаем название выбранного жанра
            genre=genres[index_]["genre"]
        except ValueError:
            print(f"{BERUSA}Invalid input.Try again.{RESET}")
            return

        # Внутренний цикл для ввода диапазона годов
        while True:
            try:
                # Ввод начального и конечного года
                year_from = int(input(f"{GREEN}From year(or 0 to reselect genre): {RESET}").strip())
                year_to = int(input(f"{GREEN}To year(or 0 to reselect genre): {RESET}").strip())
                # Возможность вернуться к выбору жанра
                if year_from==0 or year_to==0:
                    break
                # Проверка на пустой ввод
                elif not year_from or not year_to:
                    print(f"{BERUSA}Years can not be empty.{RESET}")
                    continue

                # Годы должны быть не меньше 1990
                elif year_from < 1990 or year_to < 1990:
                    print(f"{BERUSA}Invalid year, must be 1990 and greate.{RESET}")
                    continue

                # Начальный год не может быть больше конечного
                elif year_from>year_to:
                    print(f"{BERUSA}Start year must be less than or equal to end year.{RESET}")
                    continue
                break
            except ValueError:
                print(f"{BERUSA}Invalid year format.Please try again.{RESET}")
        else:
            continue        # Вернуться к выбору жанра

        # Выполняем поиск фильмов по жанру и диапазону годов
        results = db.search_film_genre_and_years(genre,year_from, year_to)
        if not results :  # Если ничего не найдено — сообщаем об этом
            print(f"{GREEN}No films found {year_from}-{year_to}. Try again.{RESET}")
            continue

        # Логируем успешный запрос
        logger.log_search("by genre and years", {"genre": genre, "year_from": year_from, "year_to": year_to}, len(results))

        # Выводим результаты постранично
        action=paginate_results(results, ["title", "release_year"])
        if action=="back": # Если пользователь выбрал "назад" — повторяем цикл для нового ввода
            continue
        elif action=="menu": # Если выбрал "меню" — выходим из функции
            return
        break






def show_popular_searches():
    """
    Выводит 5 самых популярных поисковых запросов,
    на основе количества повторений (агрегация в MongoDB).
    """
    print(f"{MAGENTA}\nTOP 5 most popular searches: \n{RESET}")
    # Получаем топ популярных запросов из базы данных
    popular=statistic.get_popular()
    # Выводим в виде таблицы
    print_table(popular,["search_type","params", "count"])

def show_last_searches():
    """
    Показывает 5 последних уникальных поисков,
    отсортированных по времени (timestamp).
    """
    print(f"{MAGENTA}\nLast 5 unique searches: \n{RESET}")
    # Получаем последние поиски из базы данных
    latest = statistic.get_latest()
    # Выводим результаты в виде таблицы
    print_table(latest, ["search_type","params", "count"])
import sys
from search_def import (
                        search_film_name,
                        search_film_year,
                        search_film_genre,
                        search_film_actor,
                        search_film_years_range,
                        search_film_genre_and_years,
                        show_popular_searches,
                        show_last_searches)
from formatter import (
                        GREEN,
                        MAGENTA,
                        RESET,
                        BERUSA
                        )


def main_menu():
    """
    Основное меню поиска фильмов.
    Возвращает выбор пользователя от 1 до 8.
    """
    search_type=[
        ["1. by title","2. by year","3. by genre"],
        ["4. by actor","5. by years (from... to...)","6. by genre and years"]
    ]

    print(f"{MAGENTA}\b\t***    WELCOME TO US   ***\n\t\tMake your choice!\n{RESET}")
    # Заголовки колонок
    print(f"{'SEARCH':<28}|{'SEARCH':<28}|{'SEARCH':<28}")
    print("_"*84)
    # Вывод пунктов меню из массива
    for row in search_type:
        print(f"{row[0]:<28}|{row[1]:<28}|{row[2]:<26}")
    print("_" * 84)
    # Дополнительные опции
    print(f"7. Show statistic")
    print("_" * 84)
    print(f"8. Go out")
    print("_" * 84)
    # Обработка ввода пользователя
    while True:
        try:
            user_choice=int(input(f"{GREEN}YOUR choice: {RESET}"))
            if user_choice not in range(1,9):
                print(f"{BERUSA}Please choose between 1 and 8.{RESET}")
                continue
            return user_choice
        except ValueError:
            print(f"{BERUSA}Please choice a number between 1 and 8.{RESET}")

def stat_menu():
    """
    Меню статистики.
    Возвращает выбор пользователя от 1 до 4.
    """
    search_static = ["1. Show popular searches list", "2. List of last searches"]
    print(f"\n\n\n{GREEN}Make your choice: {RESET}")
    print("_" * 84)
    print(f"SEARCH: {search_static[0]:<40} {search_static[1]:<40} ")
    print("_" * 84)
    print(f"{'3. Go to main menu':>26} {'4. Go out':>31}")
    print("_" * 84)
    # Обработка выбора пользователя
    while True:
        try:
            user_choice_st = int(input(f"{GREEN}YOUR choice: {RESET}"))
            if user_choice_st not in range(1, 5):
                print(f"{BERUSA}Please choose between 1 and 4.{RESET}")
                continue
            return user_choice_st
        except ValueError:
            print(f"{BERUSA}Please choose between 1 and 4.{RESET}")



def main():
    """
    Главная функция приложения.
    Управляет логикой выбора меню и вызывает соответствующие функции поиска.
    """
    while True:
        number_user_choice=main_menu()
        # Ветвление по выбору пользователя
        if number_user_choice==1:
            search_film_name()
        elif number_user_choice==2:
            search_film_year()
        elif number_user_choice==3:
            search_film_genre()
        elif number_user_choice==4:
            search_film_actor()
        elif number_user_choice==5:
            search_film_years_range()
        elif number_user_choice==6:
            search_film_genre_and_years()
        elif number_user_choice==7:
            # Подменю статистики
            while True:
                user_choice_st=stat_menu()
                if user_choice_st == 1:
                    show_popular_searches()
                elif user_choice_st == 2:
                    show_last_searches()
                elif user_choice_st==3:
                    break# Вернуться в основное меню
                elif user_choice_st==4:
                    print(f"{MAGENTA}\tGOODBY!\n See you soon.{RESET}")
                    exit()# Выход из программы
        elif number_user_choice==8:
            print(f"{MAGENTA}\tGOODBY!\n See you soon.{RESET}")
            exit()
# Точка входа
if __name__ == "__main__":
    main()
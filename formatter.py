# ANSI-коды для окраски текста в терминале
GREEN = "\033[32m"    # Зелёный цвет — используется для приглашения к вводу
MAGENTA="\033[35m"    # Пурпурный — для подзаголовков и навигации
RESET = "\033[0m"     # Сброс цвета до стандартного
BERUSA="\033[36m"     # Голубой — для информационных сообщений

def print_table(data,headers):
    """
    Печатает данные в табличном виде с заголовками.
    :param data: список словарей (строки таблицы)
    :param headers: список заголовков таблицы
    """
    if not data:
        print(f"{BERUSA}No results found.{RESET}")# Сообщение, если данных нет
        return

    # Вычисляем ширину каждой колонки по максимальной длине значений
    column=[max(len(str(row.get(h,'')))for row in data +[{h: h}])for  h in headers]

    # Печатаем строку заголовков
    header_line=" | ".join(h.ljust(w) for h,w in zip(headers,column))
    print(header_line)
    print("_"*len(header_line))

    # Печатаем строки таблицы
    for row in data :
        row_str=" | ".join(str(row.get(h,'')).ljust(w) for h,w in zip(headers,column) )
        print(row_str)

def paginate_results(data, headers,page_size=10):
    """
    Пагинация результатов: отображает данные постранично.
    :param data: список словарей
    :param headers: заголовки таблицы
    :param page_size: количество записей на странице
    """
    if not data:
        print(f"{BERUSA}No results found.{RESET}")# Если данных нет
        return

    index=0
    total_pages=(len(data)+page_size-1)//page_size
    while True:
        # Защита от выхода за границы массива
        index=max(0, min(index, (total_pages-1)*page_size))
        page=data[index:index+page_size] # Получаем текущую страницу
        print_table(page, headers)
        current_page=index//page_size+1 # Номер текущей страницы
        print(f"{MAGENTA}\nPage {current_page} of {total_pages}{RESET}")
        print(f"{MAGENTA}\nOptions: [N]next | [P]previous | [B]back | [M]menu | [Q]quit{RESET}")
        choice_pag=input(f"{GREEN}Choice: {RESET}").strip().lower()
        if choice_pag=="n": # Следующая страница
            if index + page_size<len(data):
                index+=page_size
            else:   # проверка, если нет больше страниц, выводит сообщение
                print(f"{BERUSA}End of result{RESET}")
        elif choice_pag=="p": # Предыдущая страница
            if index - page_size >=0:
                index -= page_size
            else:   # проверка, если вернулись на первую страницу, выводит сообщение
                print(f"{BERUSA}This is first page.{RESET}")
        elif choice_pag=="b":  # Назад
            return "back"
        elif choice_pag=="m":  # В главное меню
            return "menu"
        elif choice_pag=="q":  # Выход из программы
            exit()
        else:
            print(f"{BERUSA}Invalid input.{RESET}")
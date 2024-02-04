from rich.console import Console
from rich.table import Table
import json


def save_books_to_file(books, filename='library.json'):
    """
    Функция для загрузки данных при запуске программы.
    """
    with open(filename, 'w') as file:
        json.dump(books, file, indent=4)
    print(f"Данные успешно сохранены в файл '{filename}'.")


def load_books_from_file(filename='library.json'):
    """
    Функция для сохранения изменений перед выходом из программы.
    """
    try:
        with open(filename, 'r') as file:
            books = json.load(file)
        print(f"Данные успешно загружены из файла '{filename}'.")
        return books
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Создана новая библиотека.")
        return {}  # Возвращает пустой словарь, если файл не найден


def add_new_book(books, title):
    """
    Эта функция позволяет добавлять новую книгу в библиотеку.
    Пользователь вводит название, автора, жанр и количество копий книги.
    """

    author = input('Введите автора книги: ')
    genre = input('Введите жанр книги: ')

    quantity = input('Введите количество копий: ')
    while not quantity.isdigit():
        print('Неверный ввод количества. Пожалуйста, введите число.')
        quantity = input('Введите количество копий: ')
    quantity = int(quantity)


    books[title] = {'authors': [author], 'genres': [genre], 'quantity': quantity}


def add_or_update_book(books):
    title = input('Введите название книги: ')
    if title in books:
        while True:
            print(f"Книга '{title}' уже есть в базе. Выберите, что обновить:")
            print('1: Автора')
            print('2: Жанр')
            print('3: Количество копий')
            print('4: Вернуться назад')
            update_choice = input('Введите номер действия: ')

            if update_choice == '1':
                new_author = input('Введите нового автора книги: ')
                books[title]['authors'] = [new_author]

            elif update_choice == '2':
                new_genre = input('Введите новый жанр книги: ')
                books[title]['genres'] = [new_genre]

            elif update_choice == '3':
                new_quantity = input('Введите новое количество копий: ')
                while not new_quantity.isdigit():
                    print('Неверный ввод. Пожалуйста, введите число.')
                    new_quantity = input('Введите новое количество копий: ')
                books[title]['quantity'] = int(new_quantity)

            elif update_choice == '4':
                print('Возврат в предыдущее меню...')
                break

            else:
                print('Неверный выбор.')
    else:
        add_new_book(books, title)


def delete_book(books):
    while True:
        print('Выберите режим удаления:')
        print('1: Удалить конкретную книгу')
        print('2: Удалить все книги, начинающиеся с определённой буквы или цифры')
        print('3: Вернуться в главное меню')
        choice = input('Введите номер действия: ')

        if choice == '1':
            while True:
                title = input('Введите название книги для удаления (или введите "отмена" для возврата): ')
                if title.lower() == 'отмена':
                    break
                if title in books:
                    del books[title]
                    print(f'Книга "{title}" удалена из базы данных.')
                    break
                else:
                    print(f'Книга "{title}" не найдена в базе данных. Попробуйте еще раз.')

        elif choice == '2':
            start_with = input('Введите букву или цифру, с которой начинаются названия книг для удаления: ').lower()
            to_delete = [title for title in books if title.lower().startswith(start_with)]

            if not to_delete:
                print(f'Книги, начинающиеся с "{start_with}", не найдены.')
            else:
                for title in to_delete:
                    del books[title]
                print(f'Все книги, начинающиеся с "{start_with}", удалены из базы данных.')

        elif choice == '3':
            break

        else:
            print('Неверный выбор. Пожалуйста, попробуйте еще раз.')



def get_stats(books):
    """
    Отображает общее количество книг в библиотеке, суммируя количество копий каждой книги.
    """
    console = Console()
    while True:
        print('Выберите тип статистики:')
        print('1: Общее количество книг')
        print('2: Общее количество копий')
        print('3: Количество книг по жанрам')
        print('4: Количество книг по авторам')
        print('5: Вернуться в главное меню')
        choice = input('Введите номер действия: ')

        if choice in ['1', '2', '3', '4']:
            table_style = "bold green"  # Здесь можно выбрать любой подходящий стиль
            title_style = "bold green"  # Стиль для заголовка таблицы


            if choice == '1':
                table = Table(title="Общее количество книг", style=table_style, title_style=title_style)
                table.add_column('Количество книг', justify="center")
                table.add_row(str(len(books)))

            elif choice == '2':
                total_copies = sum(book['quantity'] for book in books.values())
                table = Table(title="Общее количество копий книг", style=table_style, title_style=title_style)
                table.add_column('Количество копий', justify="center")
                table.add_row(str(total_copies))

            elif choice == '3':
                genre_counts = {}
                for book in books.values():
                    for genre in book['genres']:
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
                table = Table(title="Количество книг по жанрам", style=table_style, title_style=title_style)
                table.add_column('Жанр', justify="left")
                table.add_column('Количество', justify="right")
                for genre, count in genre_counts.items():
                    table.add_row(genre, str(count))

            elif choice == '4':
                author_counts = {}
                for book in books.values():
                    for author in book['authors']:
                        author_counts[author] = author_counts.get(author, 0) + 1
                table = Table(title="Количество книг по авторам", style=table_style, title_style=title_style)
                table.add_column('Автор', justify="left")
                table.add_column('Количество', justify="right")
                for author, count in author_counts.items():
                    table.add_row(author, str(count))

            console.print(table)

        elif choice == '5':
            print('Возврат в главное меню...')
            break

        else:
            print('Неверный выбор. Пожалуйста, попробуйте еще раз.')


def search_books(books):
    """
    Позволяет искать книги по автору или жанру.
    Показывает список найденных книг, соответствующих запросу.
    """
    search_type = input('Искать по автору или жанру? (введите "автор" или "жанр"): ').lower()
    if search_type not in ['автор', 'жанр']:
        print('Неверный тип поиска. Пожалуйста, выберите "автор" или "жанр".')
        return

    search_query = input(f'Введите {"автора" if search_type == "автор" else "жанр"} для поиска: ').lower()

    found_books = []
    for title, info in books.items():
        authors = [author.lower() for author in info['authors']]
        genres = [genre.lower() for genre in info['genres']]

        if (search_type == 'автор' and any(search_query in author for author in authors)) or \
                (search_type == 'жанр' and any(search_query in genre for genre in genres)):
            found_books.append(title)

    if found_books:
        print('Найденные книги:')
        for book in found_books:
            print(book)
    else:
        print('Книги не найдены.')


def display_all_books(books):
    """
    Функция для отображения всей базы данных книг.
    """
    console = Console()
    table = Table(show_header=True, header_style='bold magenta', title='Привеееет')

    # Скорректированные ширины столбцов
    table.add_column('Название', style='dim', width=18)
    table.add_column('Авторы', width=38)
    table.add_column('Жанры', width=48)  # Уменьшите ширину, если необходимо
    table.add_column('Количество', justify='right', width=10)

    for title, details in books.items():
        authors = ', '.join(details['authors'])
        genres = ', '.join(details['genres'])
        quantity = str(details['quantity'])
        table.add_row(title, authors, genres, quantity)

    console.print(table)


def main():
    """
    Это основной цикл программы, где пользователь может выбирать
    различные действия, такие как добавление книги, очистка списка книг,
    подсчёт копий определённой книги, получение статистики и поиск книг.
    Программа продолжает работать до тех пор, пока пользователь не
    выберет опцию выхода.
    """
    books = {
        'Солярис': {
            'authors': ['Станислав Лем'],
            'genres': ['Научная фантастика', 'Психологический роман'],
            'quantity': 3
        },
        '1984': {
            'authors': ['Джордж Оруэлл'],
            'genres': ['Дистопия', 'Научная фантастика'],
            'quantity': 4
        },
        'Сумеречный дозор': {
            'authors': ['Сергей Лукьяненко', 'Владимир Васильев'],
            'genres': ['Фэнтези', 'Городское фэнтези', 'Научная фантастика'],
            'quantity': 4
        },
        'Властелин колец': {
            'authors': ['Дж. Р. Р. Толкин'],
            'genres': ['Фэнтези', 'Эпическое фэнтези'],
            'quantity': 5
        },
        'Игра престолов': {
            'authors': ['Джордж Р. Р. Мартин'],
            'genres': ['Фэнтези', 'Политический триллер'],
            'quantity': 5
        }
    }

    while True:
        print('1: Отобразить всю базу данных книг')
        print('2: Поиск книг по заданному автору или жанру')
        print('3: Добавление новых книг')
        print('4: Удаление книг из библиотеки')
        print('5: Вывод статистики по библиотеке')
        print('6: Сохранить новые данные БД')
        print('7: Загрузить актуальную версию БД')


        choice = input('\nВыберите действие: ')

        if choice == '1':
            display_all_books(books)
        elif choice == '2':
            search_books(books)
        elif choice == '3':
            add_or_update_book(books)
        elif choice == '4':
            delete_book(books)
        elif choice == '5':
            get_stats(books)
        elif choice == '6':
            save_books_to_file(books)
        elif choice == '7':
            books = load_books_from_file()
        else:
            print('Неверный выбор. Пожалуйста, попробуйте еще раз')





if __name__ == '__main__':
    main()

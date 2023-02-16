import pytest
from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
# затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
# удаление из избранного
    @pytest.mark.parametrize('base_collection', ['Гордость и предубеждение и зомби'], indirect=True)
    def test_delete_book_from_favorites_remove_and_book_from_favorites_return_empty_list(
            self, base_collection
    ):
        book_name = next(iter(base_collection.books_rating))
        base_collection.add_book_in_favorites(book_name)
        base_collection.delete_book_from_favorites(book_name)

        assert base_collection.get_list_of_favorites_books() == []

# фильрация по рейтингу
    @pytest.mark.parametrize(
        'base_collection',
        ['Чудесный нож :: Филип Пулман'],
        indirect=True,
    )
    @pytest.mark.parametrize(
        'books_with_rating',
        [
            [
                ('Кровь, пот и пиксели', 7),
                ('Гордость и предубеждение и зомби', 3),
                ('Что делать, если ваш кот хочет вас убить', 5),
                ('Пост :: Дмитрий Глуховский', 9),
            ]
        ],
    )
    @pytest.mark.parametrize('threshold', [3, 7, 9])
    def test_get_books_with_specific_rating_show_books_with_rating_above_threshold(self, base_collection,
                                                                                   books_with_rating, threshold):
        book_name = next(iter(base_collection.books_rating))
        base_collection.set_book_rating(book_name, 3)
        for book_name, book_rating in books_with_rating:
            base_collection.add_new_book(book_name)
            base_collection.set_book_rating(book_name, book_rating)

        assert base_collection.get_books_with_specific_rating(threshold) == [
            book
            for book in base_collection.books_rating
            if base_collection.get_book_rating(book) == threshold
        ]


# присваивание рейтинга
    @pytest.mark.parametrize(
        'base_collection',
        ['Пост :: Дмитрий Глуховский'],
        indirect=True,
    )
    @pytest.mark.parametrize('rating', [2, 7, 9])
    def test_set_book_rating_set_inside_add_effect(self, base_collection, rating):
        book_name = next(iter(base_collection.books_rating))
        base_collection.set_book_rating(book_name, rating)

        assert base_collection.get_book_rating(book_name) == rating

#рейтинг вне границ 1-10
    @pytest.mark.parametrize('base_collection', ['Янтарный телескоп :: Филип Пулман'], indirect=True)
    @pytest.mark.parametrize('rating', [-15, 0, 11])
    def test_set_book_rating_set_outside_margins_not_passed(self, base_collection, rating):
        # выставляем рейтинг меньше 1
        book_name = next(iter(base_collection.books_rating))
        base_collection.set_book_rating(book_name, rating)

        assert base_collection.get_book_rating(book_name) == 1

# граничные значения рейтинга 1-10
    @pytest.mark.parametrize(
        'base_collection',
        ['Северное сияние :: Филип Пулман'],
        indirect=True,
    )
    @pytest.mark.parametrize("rating", [1, 10])
    def test_set_book_rating_set_inside_margins_has_effect(self, base_collection, rating):
        book_name = next(iter(base_collection.books_rating))
        base_collection.set_book_rating(book_name, rating)

        assert base_collection.get_book_rating(book_name) == rating

#рейтинг книги не из словаря
    @pytest.mark.parametrize(
        "unknown_book", ['1984 :: Джордж Оруэлл']
    )
    def test_get_book_rating_not_in_list_return_none_rating(
            self, empty_collection, unknown_book
    ):
        assert empty_collection.get_book_rating(unknown_book) is None

#добавление книги в избранное
    @pytest.mark.parametrize(
        "base_collection", ['Мизери :: Стивен Кинг'], indirect=True
        )
    def test_add_book_in_favorites_adding_book_name_into_list_of_favorites(
        self, base_collection
        ):
        book_name = next(iter(base_collection.books_rating))
        base_collection.add_book_in_favorites(book_name)

        assert base_collection.get_list_of_favorites_books() == [book_name]

# Добаление в избранное книги вне словаря
    @pytest.mark.parametrize(
        "base_collection",
        ['Сияние :: Стивен Кинг'],
        indirect=True,
        )
    @pytest.mark.parametrize('unknown_book', ['Кладбище домашних животных :: Стивен Кинг'])
    def test_add_book_in_favorites_adding_unknown_book_has_no_effect(
        self, base_collection, unknown_book
        ):
        base_collection.add_book_in_favorites(unknown_book)

        assert base_collection.get_list_of_favorites_books() == []
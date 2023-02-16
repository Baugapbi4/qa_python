import pytest
from main import BooksCollector


@pytest.fixture(scope="function")
def empty_collection():
    collection = BooksCollector()
    return collection


@pytest.fixture(scope="function")
def base_collection(empty_collection, request):
    empty_collection.add_new_book(request.param)
    return empty_collection

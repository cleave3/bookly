from src.books.schemas import BookCreateModel

books_prefix = f"/api/v1/books"


def test_get_all_books(test_client, fake_book_service, fake_session):
    response = test_client.get(url=f"{books_prefix}")

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_create_book(test_client, fake_book_service, fake_session):
    create_book_data = {
        "title": "string",
        "author": "string",
        "published_date": "string",
        "page_count": 0,
        "language": "string",
    }

    response = test_client.post(url=f"{books_prefix}", json=create_book_data)

    assert fake_book_service.create_book_called_once_with(
        BookCreateModel(**create_book_data), fake_session
    )

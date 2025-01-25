from src.auth.schemas import UserCreateModel
from fastapi import status

auth_prefix = f"/api/v1/auth"


def test_user_creation(fake_session, fake_auth_service, test_client):

    signup_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johnddoe@mail.com",
        "password": "123456",
    }

    response = test_client.post(url=f"{auth_prefix}/signup", json=signup_data)

    assert fake_auth_service.user_exist_called_once()
    assert fake_auth_service.user_exist_called_once_with(
        signup_data["email"], fake_session
    )
    assert fake_auth_service.create_user_called_once_with(
        UserCreateModel(**signup_data), fake_session
    )
    # assert response.status_code == status.HTTP_201_CREATED

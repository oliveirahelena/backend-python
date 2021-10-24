from faker import Faker

from src.infra.test import UserRepositorySpy

from .register import RegisterUser

faker = Faker()


def test_register():
    """Testing the registry method"""

    user_repo = UserRepositorySpy()
    register_user = RegisterUser(user_repo)

    attributes = {"name": faker.name(), "password": faker.word()}

    response = register_user.register(
        name=attributes["name"], password=attributes["password"]
    )

    # Test input
    assert user_repo.insert_user_params["name"] == attributes["name"]
    assert user_repo.insert_user_params["password"] == attributes["password"]

    # Test output
    assert response["Success"] is True
    assert response["Data"]


def test_register_fail():
    """Testing the failure registry method"""

    user_repo = UserRepositorySpy()
    register_user = RegisterUser(user_repo)

    attributes = {"name": faker.random_number(digits=4), "password": faker.word()}

    response = register_user.register(
        name=attributes["name"], password=attributes["password"]
    )

    # Test input
    assert user_repo.insert_user_params == {}

    # Test output
    assert response["Success"] is False
    assert response["Data"] is None

# pylint: disable=E1101

from src.domain.models import User
from src.infra.config import DBConnectionHandler
from src.infra.entities import Users as UserModel


class UserRepository:
    """Class to manage User Repository"""

    @classmethod
    def insert_user(cls, name: str, password: str) -> User:
        """Insert data in user entity
        :param - name: person name
               - password: user password
        :return - tuple with new user inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_user = UserModel(name=name, password=password)
                db_connection.session.add(new_user)
                db_connection.session.commit()

                return User(
                    id=new_user.id, name=new_user.name, password=new_user.password
                )
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None
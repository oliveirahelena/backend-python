from typing import List

from sqlalchemy.orm.exc import NoResultFound
from src.data.interfaces import PetRepositoryInterface
from src.domain.models.pets import Pets
from src.infra.config import DBConnectionHandler
from src.infra.entities import Pets as PetsModel


class PetRepository(PetRepositoryInterface):
    """Class to manage Pet Repository"""

    @classmethod
    def insert_pet(cls, name: str, specie: str, age: int, user_id: int) -> Pets:
        """Insert data in pets entity
        :param - name: pet name
               - specie: Enum with species accepted
               - age: pet age
               - user_id: id of the pet owner(FK)
        :return - tuple with new pet inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_pet = PetsModel(name=name, specie=specie, age=age, user_id=user_id)
                db_connection.session.add(new_pet)
                db_connection.session.commit()
                return Pets(
                    id=new_pet.id,
                    name=new_pet.name,
                    specie=new_pet.specie.value,
                    age=new_pet.age,
                    user_id=new_pet.user_id,
                )

            except:
                db_connection.session.rollback()
                raise

            finally:
                db_connection.session.close()

    @classmethod
    def select_pet(cls, pet_id: int = None, user_id: int = None) -> List[Pets]:
        """Select data in pets entity by id or user_id
        :param - pet_id: id of the pet registry
        :param - user_id: owner id
        :result - List with pets
        """

        try:
            query_data = None

            if pet_id and not user_id:

                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsModel)
                        .filter_by(id=pet_id)
                        .one()
                    )
                    query_data = [data]

            elif not pet_id and user_id:

                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsModel)
                        .filter_by(user_id=user_id)
                        .all()
                    )
                    query_data = data

            elif pet_id and user_id:

                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(PetsModel)
                        .filter_by(id=pet_id, user_id=user_id)
                        .one()
                    )
                    query_data = [data]

            return query_data

        except NoResultFound:
            return []

        except:
            db_connection.session.rollback()
            raise

        finally:
            db_connection.session.close()

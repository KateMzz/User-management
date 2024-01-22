import random
import uuid
from datetime import datetime

import factory
from factory import LazyFunction, SubFactory
from faker import Faker
from passlib.context import CryptContext

from src.models.models import Group, User
from utils.db_connection import TestAsyncSessionLocal
from utils.enums import UserRole

fake = Faker()


class AbstractFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = TestAsyncSessionLocal


class GroupFactory(AbstractFactory):
    class Meta:
        model = Group

    id = factory.LazyFunction(lambda: random.randint(1, 1000000))
    name = factory.LazyFunction(fake.name)


class UserFactory(AbstractFactory):
    class Meta:
        model = User

    id = LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: "user%d" % n)
    surname = factory.Sequence(lambda n: "surname%d" % n)
    username = factory.LazyFunction(fake.user_name)
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("test")
    phone_number = factory.LazyFunction(fake.phone_number)
    email = factory.LazyFunction(fake.email)
    role = factory.Faker("random_element", elements=[elem.value for elem in UserRole])
    image_path = None
    is_blocked = False
    created_at = factory.LazyFunction(datetime.now)
    modified_at = factory.LazyFunction(datetime.now)
    group = SubFactory(GroupFactory)
    group_id = factory.SelfAttribute("group.id")


class UserFactoryNoHash:
    id = LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: "user%d" % n)
    surname = factory.Sequence(lambda n: "surname%d" % n)
    username = factory.LazyFunction(fake.user_name)
    password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("test")
    phone_number = factory.LazyFunction(fake.phone_number)
    email = factory.LazyFunction(fake.email)
    role = factory.Faker("random_element", elements=[elem.value for elem in UserRole])
    image_path = None
    is_blocked = False
    created_at = factory.LazyFunction(datetime.now)
    modified_at = factory.LazyFunction(datetime.now)
    group = SubFactory(GroupFactory)
    group_id = factory.SelfAttribute("group.id")

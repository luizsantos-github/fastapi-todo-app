from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from fastapi.testclient import TestClient
from ..models import Todos, Users
from ..main import app
from ..routers.auth import bcrypt_context

import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

# Creates a new test sqlite3 DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Creates a new local session testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# overriding methods from the API
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testadmin', 'id': 1, 'user_role': 'admin'}

# Setting the app to the test client
client = TestClient(app)

# Fixtures
@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'Test Todos',
        description = 'Test Todos description',
        priority = 5,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="testadmin",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("secret"),
        role="admin",
        phone_number="(111)-111-1111",
        id = 1
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

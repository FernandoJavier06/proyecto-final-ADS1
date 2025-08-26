# tests/conftest.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig
from app.models import User, Person, RoleEnum

@pytest.fixture(scope='function')
def app():
    """Creates an instance of the application for testing."""
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the application."""
    return app.test_client()

@pytest.fixture(scope='function')
def new_user(app):
    """Creates a test user in the database."""
    with app.app_context():
        # Crea la persona asociada
        test_person = Person(name="Test", surname="User")
        db.session.add(test_person)
        db.session.flush()

        # Crea el usuario
        test_user = User(
            userEmail="test@example.com",
            personId=test_person.personId,
            role=RoleEnum.admin
        )
        test_user.set_password("password123")
        
        db.session.add(test_user)
        db.session.commit()
        
        return test_user

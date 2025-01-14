# tests/conftest.py
import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    test_app = create_app()
    test_app.config["TESTING"] = True
    # Use an in-memory DB for testing to avoid messing up local Postgres
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with test_app.app_context():
        db.create_all()
        # Create an admin user
        admin = User(
                        username="admin",
                        password=generate_password_hash("adminpass"),
                        role="admin"
        )
        db.session.add(admin)
        # Create a normal user
        user = User(
                        username="user",
                        password=generate_password_hash("user"),
                        role="user"
        )
        db.session.add(user)
        db.session.commit()

        yield test_app

        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

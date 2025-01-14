"""
Defines the User model, representing user like admin user
or normal user
"""
from app import db


class User(db.Model):
    """
    Represents a registered User

    Attributes:
        id (int): Primary key.
        username (str): User's name
        password (str): User's password
        role (str): Role of a user whether admin or normal user
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # 'admin' or 'user'

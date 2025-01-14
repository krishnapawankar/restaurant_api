"""
Defines the Restaurant model, representing restaurant data
in the database.
"""

import enum
from app import db


class PriceRange(enum.Enum):
    """
    Enumerates the possible price ranges for a restaurant.
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Restaurant(db.Model):
    """
    Represents a restaurant in the system.

    Attributes:
        id (int): Primary key.
        name (str): The restaurant's name.
        cuisine_type (str): Type of cuisine (Italian, Indian, etc.).
        address (str): Physical address.
        price_range (PriceRange): Enum indicating price range.
    """
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.Enum(PriceRange), nullable=False)

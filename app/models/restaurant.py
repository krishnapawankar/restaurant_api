# app/models/restaurant.py
from app import db
import enum


class PriceRange(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.Enum(PriceRange), nullable=False)

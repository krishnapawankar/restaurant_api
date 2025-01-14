"""
Defines the Review model, representing customer reviews
for restaurants.
"""

import enum
from datetime import date

from app import db


class ReviewStatus(enum.Enum):
    """
    Enumerates the possible statuses for a review (e.g., PENDING, APPROVED).
    """
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class Review(db.Model):
    """
    Represents a review posted by a user for a given restaurant.

    Attributes:
        id (int): Primary key.
        restaurant_id (int): Foreign key referencing Restaurant.
        rating (int): Star rating (1-5).
        comment (str): User's comment on the restaurant.
        visit_date (date): Date of visit.
        status (ReviewStatus): Whether the review is pending or approved.
    """
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(
                                db.Integer,
                                db.ForeignKey("restaurant.id"),
                                nullable=False
    )
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.String(500), nullable=True)
    visit_date = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(
                        db.Enum(ReviewStatus),
                        default=ReviewStatus.PENDING,
                        nullable=False
    )

    # Relationship
    restaurant = db.relationship("Restaurant", backref="reviews")

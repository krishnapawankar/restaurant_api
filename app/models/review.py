# app/models/review.py
from app import db
import enum
from datetime import date

class ReviewStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.String(500), nullable=True)
    visit_date = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(db.Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    # Relationship
    restaurant = db.relationship("Restaurant", backref="reviews")

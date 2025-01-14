# app/api/analytics.py
from flask_restx import Namespace, Resource
from sqlalchemy import desc, func

from app import db
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.utils.cache import cache

analytics_ns = Namespace('analytics', description="Analytics Endpoints")


@analytics_ns.route('/average-ratings')
class AverageRatings(Resource):
    @cache.cached(timeout=120)  # Cache for 120 seconds
    def get(self):
        """
        Returns the average rating per restaurant:
        [
          {
            "restaurant_id": 1,
            "average_rating": 4.2
          },
          ...
        ]
        (Uses caching to speed up repeated requests.)
        """
        results = (
            db.session.query(
                Review.restaurant_id,
                func.avg(Review.rating).label("avg_rating")
            )
            .group_by(Review.restaurant_id)
            .all()
        )

        data = [
            {"restaurant_id": r.restaurant_id,
             "average_rating": float(r.avg_rating)}
            for r in results
        ]
        return data, 200


@analytics_ns.route('/top-3/<string:cuisine_type>')
class Top3Restaurants(Resource):
    @cache.cached(timeout=120)
    def get(self, cuisine_type):
        """
        Returns top 3 restaurants by cuisine type,
        sorted by average rating (desc).
        [
          {
            "restaurant_id": 1,
            "name": "ABC",
            "cuisine_type": "Italian",
            "average_rating": 4.5
          },
          ...
        ]
        """
        subq = (
            db.session.query(
                Review.restaurant_id.label("rest_id"),
                func.avg(Review.rating).label("avg_rating")
            )
            .group_by(Review.restaurant_id)
            .subquery()
        )

        results = (
            db.session.query(Restaurant.id, Restaurant.name,
                             Restaurant.cuisine_type, subq.c.avg_rating)
            .join(subq, subq.c.rest_id == Restaurant.id, isouter=True)
            .filter(Restaurant.cuisine_type.ilike(cuisine_type))
            .order_by(desc(subq.c.avg_rating))
            .limit(3)
            .all()
        )

        data = []
        for row in results:
            data.append({
                "restaurant_id": row.id,
                "name": row.name,
                "cuisine_type": row.cuisine_type,
                "average_rating":
                    float(row.avg_rating) if row.avg_rating else 0.0
            })
        return data, 200

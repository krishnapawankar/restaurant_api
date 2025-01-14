# app/api/reviews.py
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.models.review import Review, ReviewStatus
from app.models.restaurant import Restaurant
from app.schemas.review import ReviewSchema
from app.utils.exceptions import NotFoundError

review_ns = Namespace('reviews', description="Review Management")

review_model = review_ns.model('Review', {
    'id': fields.Integer(readonly=True),
    'restaurant_id': fields.Integer(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'comment': fields.String(),
    'visit_date': fields.String(description="YYYY-MM-DD"),
    'status': fields.String(readonly=True, enum=["PENDING", "APPROVED"])
})

# NEW: model specifically for PATCH request body
review_patch_model = review_ns.model('ReviewPatch', {
    'status': fields.String(required=True, enum=["PENDING", "APPROVED"])
})

@review_ns.route('')
class ReviewList(Resource):
    @jwt_required()
    @review_ns.expect(review_model)
    def post(self):
        """Submit a new review (status=PENDING by default)."""
        schema = ReviewSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        restaurant = Restaurant.query.get(data["restaurant_id"])
        if not restaurant:
            raise NotFoundError("Restaurant does not exist.")

        visit_date = data.get("visit_date", datetime.now().date())

        review = Review(
            restaurant_id=restaurant.id,
            rating=data["rating"],
            comment=data.get("comment", ""),
            visit_date=visit_date
        )
        db.session.add(review)
        db.session.commit()

        return schema.dump(review), 201

    def get(self):
        """Retrieve all reviews (paginated)."""
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        paginated = Review.query.paginate(page=page, per_page=per_page, error_out=False)

        schema = ReviewSchema(many=True)
        return {
            "reviews": schema.dump(paginated.items),
            "total": paginated.total,
            "pages": paginated.pages,
            "page": paginated.page
        }, 200


@review_ns.route('/<int:review_id>')
class ReviewDetail(Resource):
    @jwt_required()
    def get(self, review_id):
        """Retrieve a single review by ID."""
        review = Review.query.get(review_id)
        if not review:
            raise NotFoundError("Review not found.")

        schema = ReviewSchema()
        return schema.dump(review), 200

    @jwt_required()
    @review_ns.expect(review_patch_model, validate=True)
    def patch(self, review_id):
        """Update a review's status (admin only)."""
        # current_user = get_jwt_identity()
        claims = get_jwt()  # returns the entire claims dict
        user_role = claims["role"]  # "admin" or "user"

        if user_role != "admin":
            return {"message": "Admin privilege required."}, 403

        review = Review.query.get(review_id)
        if not review:
            raise NotFoundError("Review not found.")

        new_status = request.json.get("status")
        if new_status and new_status in ReviewStatus._member_names_:
            review.status = ReviewStatus[new_status]
            db.session.commit()
            return {"message": "Review status updated."}, 200

        return {"message": "Invalid status."}, 400

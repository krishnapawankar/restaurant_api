"""
Manages restaurant-related endpoints (CRUD).
Requires admin privileges for creation.
"""

from flask import request
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

from app import db
from app.models.restaurant import PriceRange, Restaurant
from app.schemas.restaurant import RestaurantSchema
from app.utils.exceptions import NotFoundError
from app.utils.limiter import limiter

restaurant_ns = Namespace(
    'restaurants',
    description="Restaurant Management",
    # specify that this entire namespace requires JWT
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    security='Bearer'
)

restaurant_model = restaurant_ns.model('Restaurant', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'cuisine_type': fields.String(required=True),
    'address': fields.String(required=True),
    'price_range': fields.String(
        required=True,
        enum=["LOW", "MEDIUM", "HIGH"]
    ),
})


@restaurant_ns.route('')
class RestaurantList(Resource):
    """
    Resource for listing and creating restaurants.
    """
    method_decorators = [limiter.limit("10/minute")]

    @restaurant_ns.doc(
        params={'page': 'Page number',
                'per_page': 'Items per page'}
    )
    def get(self):
        """
        Retrieves a list of restaurants.
        Supports pagination via query params: ?page=1&per_page=5

        Returns:
            JSON list of restaurants plus pagination info.
        """
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        paginated = Restaurant.query.paginate(
                                                page=page,
                                                per_page=per_page,
                                                error_out=False
        )
        schema = RestaurantSchema(many=True)

        return {
            "restaurants": schema.dump(paginated.items),
            "total": paginated.total,
            "pages": paginated.pages,
            "page": paginated.page
        }, 200

    @jwt_required()
    @restaurant_ns.expect(restaurant_model)
    def post(self):
        """
        Creates a new restaurant. Only admin users can perform this action.

        Returns:
            The created restaurant in JSON with status code 201.
        """
        claims = get_jwt()  # returns the entire claims dict
        user_role = claims["role"]  # "admin" or "user"
        if user_role != "admin":
            return {"message": "Admin privilege required."}, 403

        schema = RestaurantSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        price_enum = PriceRange(data["price_range"])
        new_restaurant = Restaurant(
            name=data["name"],
            cuisine_type=data["cuisine_type"],
            address=data["address"],
            price_range=price_enum
        )
        db.session.add(new_restaurant)
        db.session.commit()

        return schema.dump(new_restaurant), 201


@restaurant_ns.route('/<int:restaurant_id>')
class RestaurantDetail(Resource):
    """
    Resource for retrieving a single restaurant by ID.
    """
    @jwt_required(optional=True)
    def get(self, restaurant_id):
        """
        Retrieves a specific restaurant by ID.

        Args:
            restaurant_id (int): The ID of the restaurant to retrieve.

        Returns:
            The restaurant data in JSON if found, or a 404 error if not found.
        """
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            raise NotFoundError("Restaurant not found.")

        schema = RestaurantSchema()
        return schema.dump(restaurant), 200

"""
Marshmallow schema for validating and serializing Restaurant data.
"""

from marshmallow import Schema, fields


class RestaurantSchema(Schema):
    """
    Validates and serializes Restaurant data.

    Attributes:
        id (int): Read-only field for the primary key.
        name (str): Required restaurant name.
        cuisine_type (str): Required cuisine type.
        address (str): Required address.
        price_range (PriceRange): Required price range (LOW, MEDIUM, HIGH).
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    cuisine_type = fields.Str(required=True)
    address = fields.Str(required=True)
    price_range = fields.Str(required=True)  # "LOW", "MEDIUM", "HIGH"

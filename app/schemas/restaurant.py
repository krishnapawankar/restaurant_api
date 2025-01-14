# app/schemas/restaurant.py
from marshmallow import Schema, fields

class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    cuisine_type = fields.Str(required=True)
    address = fields.Str(required=True)
    price_range = fields.Str(required=True)  # "LOW", "MEDIUM", "HIGH"

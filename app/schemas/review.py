# app/schemas/review.py
from marshmallow import Schema, fields

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    restaurant_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    comment = fields.Str()
    visit_date = fields.Date()
    status = fields.Str(dump_only=True)

"""
Marshmallow schema for validating and serializing Reviews data.
"""

from marshmallow import Schema, fields


class ReviewSchema(Schema):
    """
    Validates and serializes Reviews data.

    Attributes:
        id (int): Read-only field for the primary key.
        restaurant_id (int): Required restaurant id.
        rating (int): Required review rating.
        comment (str): Required Review comments.
        visit_date (date): Restaurant visited date
        status (str): Status of review pending/approved
    """
    id = fields.Int(dump_only=True)
    restaurant_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    comment = fields.Str()
    visit_date = fields.Date()
    status = fields.Str(dump_only=True)

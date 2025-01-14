"""
Marshmallow schema for validating and serializing user data
"""

from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    Validates and Serializes registered User data

    Attributes:
        id (int): Primary key.
        username (str): User's name
        password (str): User's password
        role (str): Role of a user whether admin or normal user
    """

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    role = fields.Str(dump_only=True)

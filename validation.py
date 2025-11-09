
from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class UserSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50, error="Name length between 1 and 50"), error_messages={"required":"Name is required"})
    surname = fields.String(required=True, validate=validate.Length(min=1, max=50, error="Surname length between 1 and 50"), error_messages={"required":"Surname is required"})
    email = fields.Email(required=True, error_messages={"required":"Email is required", "invalid":"Email is invalid"})
    password = fields.String(required=True, validate=validate.Length(min=8, error="Password minimal length 8"), error_messages={"required":"Password is required"})
    confirmPassword = fields.String(required=True, error_messages={"required":"ConfirmPassword is required"})

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        if data.get("password") != data.get("confirmPassword"):
            raise ValidationError("Passwords must be the same", field_name="confirmPassword")
        
userSchema = UserSchema()
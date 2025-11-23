
import datetime
from marshmallow import Schema, fields, validate, ValidationError, validates_schema, validates


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

class ChangingPasswordSchema(Schema):
    password = fields.String(required=True, validate=validate.Length(min=8, error="New password minimal length 8"), error_messages={"required":"New password is required"})
    confirmPassword = fields.String(required=True, error_messages={"required":"ConfirmPassword is required"})

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        if data.get("password") != data.get("confirmPassword"):
            raise ValidationError("Passwords must be the same", field_name="confirmPassword")
        
changingPasswordSchema = ChangingPasswordSchema()

class ChangingEmailSchema(Schema):
    email = fields.Email(required=True, error_messages={"required":"Email is required", "invalid":"Email is invalid"})

changingEmailSchema = ChangingEmailSchema()

class ChangingUserDataSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50, error="Name length between 1 and 50"), error_messages={"required":"Name is required"})
    surname = fields.String(required=True, validate=validate.Length(min=1, max=50, error="Surname length between 1 and 50"), error_messages={"required":"Surname is required"})

changingUserDataSchema = ChangingUserDataSchema()

class VoteSchema(Schema):
    voteTitle = fields.String(required=True, validate=validate.Length(min=1, max=50, error="vote title length between 1 and 50"), error_messages={"required":"vote title is required"})
    startDate = fields.DateTime(required=True, error_messages={"required":"start date is required", "invalid" : "start date is invalid"})
    endDate = fields.DateTime(required=True, error_messages={"required":"end date is required", "invalid" : "end date is invalid"})
    description = fields.String(required=True, validate=validate.Length(min=1, max=65535, error="description length between 1 and 65535"), error_messages={"required":"description is required"})
    realTimeResults = fields.Boolean(required=False)
    voteOptions = fields.List(
        fields.String(validate=validate.Length(min=0, max=100, error="description length between 1 and 65535")),
        required=True,
        error_messages={"required":"vote options is required"},
    )

    @validates("voteOptions")
    def validate_vote_options(self, value, **kwargs):
        for el in value:
            if len(el) < 1 or len(el) > 100:
                raise ValidationError("all vote options must be between 1 and 100 characters.")


    @validates("startDate")
    def validate_start_date(self, value, **kwargs):
        if value < datetime.datetime.today():
            raise ValidationError("start date can't be in past")
        
    @validates("endDate")
    def validate_end_date(self, value, **kwargs):
        if value < datetime.datetime.today():
            raise ValidationError("end date can't be in past")
        
    @validates_schema
    def validate_date_valid(self, data, **kwargs):
        if data.get("endDate") < data.get("startDate"):
            raise ValidationError("Invalid dates values", field_name="date")

voteSchema = VoteSchema()
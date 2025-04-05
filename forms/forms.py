from flask_wtf import FlaskForm
import uuid
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp

class VerifyAccountForm(FlaskForm):
    owner = StringField("Account Owner", validators=[DataRequired(), Length(max=100)])
    bank_account_number = StringField("Account Number", validators=[DataRequired(), Length(max=20)])
    wallet_id = StringField("Wallet ID", validators=[DataRequired(), Length(max=50)])

def validate_uuid(form, field):
    try:
        uuid_obj = uuid.UUID(field.data, version=4)  # Ensure it's a valid UUIDv4
    except ValueError:
        raise ValidationError("Invalid link id format.")

class OTPforLinkForm(FlaskForm):
    link_id = StringField("Link ID", validators=[DataRequired(), validate_uuid])
    otp = StringField("OTP", validators=[DataRequired(),  Regexp(r'^\d{6}$', message="OTP must be of 6 digit numbers")])

class VerifyTransactionForm(FlaskForm):
    amount = StringField("Amount", validators=[DataRequired(), Regexp(r"^\d{1,10}(\.\d{1,2})?$", message="Invalid amount format or too small amount and too large amount.")])
    token = StringField("Token", validators=[DataRequired(), Length(max=1024)])

class OTPTransactionForm(FlaskForm):
    transaction_id = StringField("Transaction No", validators=[DataRequired(), validate_uuid])
    otp = StringField("OTP", validators=[DataRequired(),  Regexp(r'^\d{6}$', message="OTP must be of 6 digit numbers")])

from services.users import CreateUser, GetUser, GetUserIdByPhone
from services.accounts import *
from services.link_bank import *
from services.withdraw_for_wallet import *


def register_routes(api):
    
    api.add_resource(CreateUser, "/api/users")
    api.add_resource(GetUser, "/api/users/<int:user_id>")
    api.add_resource(GetUserIdByPhone, "/api/users/get_user_by_phone")


    api.add_resource(CreateAccount, "/api/accounts")
    api.add_resource(GetBalance, "/api/accounts/<account_number>/balance")
    api.add_resource(GetAllUserAccounts, "/api/accounts/all/<int:user_id>")

    api.add_resource(VerifyBankAccount, "/api/verify_bank_account")
    api.add_resource(VerifyOTPForLinkBank, "/api/verify_otp_link_bank")

    api.add_resource(VerifyTransaction, "/api/verify_transaction")
    api.add_resource(VerifyOTPWithdraw, "/api/verify_otp_withdraw")
class ResponseHandler:
    # Predefined response codes and messages
    RESPONSE_CODES = {
        "S001": "Operation Successful",
        "E001": "Invalid bank account",
        "E002": "Invalid Input",
        "E003": "Wrong account owner name",
        "E004": "Invalid OTP or link ID",
        "E005": "Insufficient balance",
        "E006": "Invalid OTP"
    }

    @staticmethod
    def generate(response_code, data=None):
        """
        Generate a standardized JSON response.

        :param response_code: The response code (e.g., "S001")
        :param data: The actual data to be returned (default: None)
        :return: Flask JSON response
        """
        response_message = ResponseHandler.RESPONSE_CODES.get(response_code, "Unknown response code")
        response_body = {
            "responseCode": response_code,
            "responseMessage": response_message,
            "data": data
        }
        return response_body, 200 if response_code.startswith("S") else 400  # Success -> 200, Error -> 400

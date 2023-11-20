import jwt
import inspect
from datetime import datetime, timedelta, timezone

SECRET_KEY = "a6U7MEQ6rzasJz4A"

def jwt_token_generate(payload: dict):
    """
    Generates a JWT token with the provided payload.

    Args:
        :payload (dict): A dictionary containing the user's information.

    Returns:
        dict: A dictionary containing information about the generated token.
    """
    try:
        payload.pop('password', '')
        user = payload.copy()
        user.update({
            "id": payload['id'],
            "nombre": payload['nombre'],
            "rol": payload['rol'],
            "email": payload['email'],
            "exp": due_date_generate(days=1, seconds=30),
        })

        token = jwt.encode(user, SECRET_KEY, algorithm="HS256")

        userSession = {
            "status": True,
            "userSession": 1,
            "idToken": token,
            "payload": payload,
            "message": "Successfully generated token",   
        }
        return userSession

    except Exception as e:
        return map_error(e, "Error generating token", "GenerateTokenException", 500)


def verify_token(token) -> dict:
    """
    Verifies the authenticity of a JWT token.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        dict: A dictionary indicating the result of the token verification.
    """
    
    try:

        is_valid = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        
        if is_valid:
            
            response = {
                "status": True,
                "message": "Token verification successful",
                "data": is_valid
            }

            return response 
        else:
            raise ValueError([])
        
    except ValueError as e:
        return map_error(e, "Invalid Token", "InvalidTokenError", 102)
    except jwt.ExpiredSignatureError as e:
        return map_error(e, "Expired token", "ExpiredSignatureError", 101)
    except jwt.exceptions.InvalidSignatureError as e:
        return map_error(e, "Token signature is invalid", "InvalidSignatureError", 102)
    except jwt.exceptions.InvalidTokenError as e:
        return map_error(e, "Invalid Token", "InvalidTokenError", 102)
    except jwt.exceptions.InvalidKeyError as e:
        return map_error(e, "Invalid Token Secret Key", "InvalidKeyError", 102)
    

def due_date_generate(days=0, hours=0, minutes=0, seconds=60) -> float:

    """
    Generates a due date based on the specified time intervals.

    Args:
        days (int, optional): Number of days. Defaults to 0.
        hours (int, optional): Number of hours. Defaults to 0.
        minutes (int, optional): Number of minutes. Defaults to 0.
        seconds (int, optional): Number of seconds. Defaults to 60.

    Returns:
        float: The timestamp of the due date.
    """

    current_date = datetime.now(tz=timezone.utc)
    due_time = timedelta(days, hours, minutes, seconds)
    due_date = datetime.timestamp(current_date + due_time)

    return due_date


def map_error(error, message, error_message, error_code=None) -> dict:

    """
    Maps an error to a structured response format.

    Args:
        error (Exception): The raised exception.
        message (str): A descriptive message for the response.
        error_message (str): An error identifier for the response.
        error_code (int, optional): An error code. Defaults to None.

    Returns:
        dict: A structured response indicating the error.
    """

    jwt_error = bool(len(error.args) > 1)
    print(error)

    response = {
        "status": False,
        "errorMessage": error_message,
        "message": message,
    }


    return response
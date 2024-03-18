import hashlib
import uuid
import jwt
from datetime import datetime, timedelta

blacklist = {}


class InfoAuth:
    def __init__(self, id, role, username, password):
        self.id = id
        self.role = role
        self.username = username
        self.password = password


def generate_token(info_auth):
    claims = {
        "iss": "http://127.0.0.1:8002",
        "sub": info_auth.id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "jti": str(uuid.uuid4()),
        "role": info_auth.role
    }
    secret_key = "cheie"
    token = jwt.encode(claims, secret_key, algorithm="HS256")
    return token


def validate_token(token_response):
    try:
        token = token_response.token
        secret_key = "cheie"
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        current_time = datetime.utcnow()
        exp_time = datetime.utcfromtimestamp(decoded_token.get("exp", 0))

        if exp_time < current_time:
            blacklist[token] = "expired"
            return "Procesare cu succes. Token expirat"

        return "Validarea s-a realizat cu succes!\n" + "sub " + decoded_token.get("sub") + "\nrole " + decoded_token.get("role")
    except jwt.ExpiredSignatureError:
        blacklist[token] = "expired"
        return "Procesare cu succes. Token expirat"
    except jwt.InvalidTokenError:
        blacklist[token] = "corrupt"
        return "Procesare cu succes. Token invalid"


def destroy_token(token_response):
    token = token_response.token
    blacklist[token] = "destroyed"
    return "Procesarea de distrugere s-a realizat cu succes!"
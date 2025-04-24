import jwt

#generate a token for log in
def generate_token(payload: dict, secret_key: str):
    if not isinstance(secret_key, str):
        raise ValueError("Secret key must be a string")
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

#decode a token
def decode_token(token: str, secret_key: str):
    if not isinstance(secret_key, str):
        raise ValueError("Secret key must be a string")
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Token is invalid")


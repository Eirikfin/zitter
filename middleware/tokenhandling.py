import jwt  # PyJWT library

#generate a token for log in
def generate_token(payload: dict, secret_key: str):
    if not isinstance(secret_key, str):
        raise ValueError("Secret key must be a string")
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

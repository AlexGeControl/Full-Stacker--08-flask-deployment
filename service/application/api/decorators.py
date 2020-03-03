import datetime
import jwt

from flask import abort, request

from functools import wraps

#  JWT ERROR
#  ----------------------------------------------------------------
class JWTError(Exception):
    """ exception for JWT processing
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

#  ENCODING
#  ----------------------------------------------------------------
def get_contents():
    """ obtains the account info
    """
    # parse POSTed contents:
    contents = request.get_json()

    # get email and password:
    email = contents.get('email', None)
    if email is None:
        raise JWTError(
            {
                'code': 'invalid_data',
                'description': 'Missing parameter: email'
            }, 
            400
        )

    password = contents.get('password', None)
    if password is None:
        raise JWTError(
            {
                'code': 'invalid_data',
                'description': 'Missing parameter: password'
            }, 
            400
        )
    
    # formate:
    contents = {
        'email': email, 
        'password': password
    }

    return contents

def encode_jwt(payload, key, algorithm = 'HS256'):
    """ generate JWT:
    """
    # set expiration time:
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)

    # create payload:
    payload = {
        'nbf': datetime.datetime.utcnow(),
        'exp': expiration_time,
        'email': payload['email']
    }

    # create token:
    token = jwt.encode(
        payload, 
        key, 
        algorithm=algorithm
    )

    return token

def requires_contents(logger, key, algorithm = 'HS256'):
    """ decorator for token generation contents processing
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # get contents:
                contents = get_contents()
                # authentication:
                token = encode_jwt(contents, key, algorithm)
            except JWTError as e:
                # add to log:
                logger.error(e.error["description"])
                # abort:
                abort(e.status_code, description=e.error["description"])
            return f(token, *args, **kwargs)
        return decorated_function
    return decorator

#  DECODING
#  ----------------------------------------------------------------
def get_token():
    """ obtains the JWT token from the Authorization header
    """
    # get authorization header:
    auth = request.headers.get('Authorization', None)
    
    # authorization header should be included:
    if auth is None:
        raise JWTError(
            {
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 
            401
        )
    
    # authorization header should be 'Bearer [JWT]'
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise JWTError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 
            401
        )
    elif len(parts) == 1:
        raise JWTError(
            {
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 
            401
        )
    elif len(parts) > 2:
        raise JWTError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 
            401
        )

    # extract JWT:
    token = parts[1]

    return token


def decode_jwt(encoded, key, algorithms = 'HS256'):
    """ verify and decode JWT
    """
    try:
        payload = jwt.decode(
            encoded, 
            key, 
            algorithms = algorithms
        )

        return payload
    # if token has expired:
    except jwt.exceptions.ExpiredSignatureError:
        raise JWTError(
            {
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 
            401
        )
    # other exceptions:
    except Exception:
        raise JWTError(
            {
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 
            400
        )

def requires_auth(logger, key, algorithms = 'HS256'):
    """ decorator for authentication header processing
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # get JWT token:
                token = get_token()
                # authentication:
                payload = decode_jwt(token, key, algorithms)
            except JWTError as e:
                # add to log:
                logger.error(e.error["description"])
                # abort:
                abort(e.status_code, description=e.error["description"])
            return f(payload, *args, **kwargs)
        return decorated_function
    return decorator
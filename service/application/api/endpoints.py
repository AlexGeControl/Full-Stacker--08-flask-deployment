from . import bp

from flask import jsonify

from .decorators import requires_contents, requires_auth

from config import config

#  HEALTH CHECK
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET', 'POST'])
def health():
    """ endpoint for health check
    """
    return jsonify("Healthy")

#  ENCODING
#  ----------------------------------------------------------------
@bp.route('/auth', methods=['POST'])
@requires_contents(
    logger = config['default'].LOGGER,
    key = config['default'].JWT_SECRET,
    algorithm = config['default'].JWT_ALGORITHMS
)
def auth(token):
    """ endpoint for JWT generation using POSTed email and password
    """
    return jsonify(
        token=token.decode('utf-8')
    )

#  DECODING
#  ----------------------------------------------------------------
@bp.route('/contents', methods=['GET'])
@requires_auth(
    logger = config['default'].LOGGER,
    key = config['default'].JWT_SECRET,
    algorithms = config['default'].JWT_ALGORITHMS
)
def contents(payload):
    """ endpoint for JWT payload decoding
    """
    # format response:
    response = {
        'email': payload['email'],
        'exp': payload['exp'],
        'nbf': payload['nbf'] 
    }

    return jsonify(**response)
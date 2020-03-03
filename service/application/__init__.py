from flask import Flask

from flask_cors import CORS

from config import basedir, config

cors = CORS()

#  APP FACTORY
#  ----------------------------------------------------------------
def create_app(config_name):
    # config static path:
    app = Flask(
        __name__,
        static_url_path = '/static', static_folder = 'static'
    )
    # load configs:
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)    
    
    # enable CORS:
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    """

    # attach routes and custom error pages here
    
    #  api
    #  ----------------------------------------------------------------  
    from .api import bp as blueprint_api
    app.register_blueprint(blueprint_api, url_prefix='/api/v1')

    return app
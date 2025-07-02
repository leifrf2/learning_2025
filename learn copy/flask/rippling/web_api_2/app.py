from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from routes import app_blueprint

def create_app():
    app = Flask(__name__)
    app.config['APPLICATION_ROOT'] = '/foo'

    app.register_blueprint(app_blueprint, prefix_url="/auth")

    jwt = JWTManager(app)    
    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)

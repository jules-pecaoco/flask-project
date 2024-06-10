from flask import Flask, redirect, url_for
from app.home.routes import home as home_blueprint
from app.auth.routes import auth as auth_blueprint

def create_app():
    app = Flask(__name__)

    # Register the main blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')

    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app


# Create the app instance
app = create_app()

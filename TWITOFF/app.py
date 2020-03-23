from flask import Flask
from .models import DB

# Now, we want to make an app factory.


def create_app():
    app = Flask(__name__)

    # Add our config
    app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///db.sqlite3')

    # Have the database know about the app.
    DB.init_app(app)

    @app.route('/')
    def route():
        return 'Welcome to Twitoff!'
    return app

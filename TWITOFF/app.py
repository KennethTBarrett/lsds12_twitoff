from decouple import config
from flask import Flask, render_template, request
from .models import DB, User


# Now, we want to make an app factory.

def create_app():
    app = Flask(__name__)

    # Add our config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Have the database know about the app.
    DB.init_app(app)

    @app.route('/')
    def route():
        users = User.query.all()
        return render_template('index.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('index.html', title='Reset', users=[])

    return app

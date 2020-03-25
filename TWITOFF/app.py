"""Build app factory and do routes / configuration """

from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user


# Now, we want to make an app factory.

def create_app():
    app = Flask(__name__)

    # Add our config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Have the database know about the app.
    DB.init_app(app)

    # Route for index page.
    @app.route('/')
    def route():
        users = User.query.all()
        return render_template('index.html', title='Home', users=users)

    # New route to get users or get users.
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User: {} has been successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding user: {} &nbsp; Error: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets)

    # Route for predictions.
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves.'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])

            message = "{}".format(request.values['tweet_text'] +
                                  " is more likely to be said by " +
                                  "{} than {}".format(user2 if prediction
                                                      else user1, user1 if
                                                      prediction else user2))
        return render_template('prediction.html', title='Prediction',
                               message=message)

# Route for page to reset database to scratch.
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('index.html', title='Reset', users=[])

    return app

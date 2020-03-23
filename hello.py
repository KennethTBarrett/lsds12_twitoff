'''Minimal Flask App'''

from flask import Flask


# Make the Application
app = Flask(__name__)

# Make the route
@app.route("/")

# Make and define a function
def hello():
    return 'Hello, beautiful world!'
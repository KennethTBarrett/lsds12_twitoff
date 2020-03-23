'''Minimal Flask App'''

from flask import Flask, render_template


# Make the Application
app = Flask(__name__)

# Make the route
@app.route("/")

# Make and define a function
def hello():
    return render_template('home.html')

# Make another route
@app.route("/about")

# Make another function
def about():
    return render_template('about.html')

from flask import Flask

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Jimbert Bingus",
        "about" :"Mom help I don't know how react works"
    }

    return response_body
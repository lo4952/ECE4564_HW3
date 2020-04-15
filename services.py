#!/usr/bin/env

import sys, ServicesKeys
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

if (len(sys.argv) != 3):
	sys.exit("Error: Syntax is 'services.py -p <port number>'")

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("secret"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

@app.route('/Canvas', methods=['GET'])
def get_canvas():
	return "Canvas Request"

@app.route('/Marvel', methods=['GET'])
def get_marvel():
	return "Marvel Request"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[2], debug=True)

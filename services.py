#!/usr/bin/env

import sys, time, hashlib, requests, ServicesKeys
from flask import Flask
from flask import request
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
@auth.login_required
def get_canvas():
	if 'file' in request.args:
		url = "https://vt.instructure.com/api/v1/courses/%s/files/?search_term=%s&access_token=%s" % (104692, request.args['file'], ServicesKeys.c_token)
		file = requests.get(url)
		with open(request.args['file'], 'wb') as f:
			f.write(file.content)
		return "File Downloaded \n"
	else:
		return "Error: File Not Found \n"

@app.route('/Marvel', methods=['GET'])
@auth.login_required
def get_marvel():
	if 'story' in request.args:
		t = time.strftime("%Y%d%m%H%M%S")
		m = hashlib.md5()
		m.update("{}{}{}".format(t, ServicesKeys.m_pri, ServicesKeys.m_pub).encode("utf-8"))
		hash = m.hexdigest()
		file = requests.get('https://gateway.marvel.com/v1/public/stories/{}?apikey={}&hash={}&ts={}'.format(request.args['story'], ServicesKeys.m_pub, hash, t))
		print(file.text)
		with open(request.args['story'], 'wb') as f:
			f.write(file.content)
		return "File Downloaded \n"
	else:
		return "Error: File Not Found \n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[2], debug=True)

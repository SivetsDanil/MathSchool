# НУЖНО УСТАНОВИТЬ requirements.txt командой 'pip install -r requirements.txt'
from flask_login import LoginManager, login_required, logout_user
from flask import render_template, redirect
from api import indexAPI
import os
from flask import Flask, request, jsonify
from flask import send_from_directory
from databaseAPI import get_tutors_by_subject, init_db

from flask_login import current_user
import hashlib
import time




application = Flask(__name__, static_folder='static', static_url_path='/static')
application.config['SECRET_KEY'] = "Secret"
LICENSE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'docs')

login_manager = LoginManager()
login_manager.init_app(application)

init_db()





class User:
    def __init__(self, id):
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User(id=1)

@application.route('/license')
def license_pdf():
    return send_from_directory(
        os.path.join(application.root_path, 'static', 'docs'),
        'license.pdf',
        mimetype='application/pdf'
    )


@application.route('/api/tutors')
def get_tutors():
    subject = request.args.get('subject', '')
    tutors = get_tutors_by_subject(subject)
    return jsonify(tutors)

@application.route("/")
def index():
    return render_template('index.html')


def main():
    application.run(host='0.0.0.0', port='8100')

if __name__ == '__main__':
    main()
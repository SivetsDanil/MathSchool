# НУЖНО УСТАНОВИТЬ requirements.txt командой 'pip install -r requirements.txt'
from flask_login import LoginManager, login_required, logout_user
from flask import render_template, redirect
from api import indexAPI
import os
from flask import Flask, request, jsonify
from flask import send_from_directory
from databaseAPI import get_tutors_by_subject
from flask_login import current_user
import hashlib
import time




application = Flask(__name__, static_folder='static', static_url_path='/static')
application.config['SECRET_KEY'] = "Secret"
LICENSE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'docs')

login_manager = LoginManager()
login_manager.init_app(application)






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


@application.route('/form', methods=['POST'])
def handle_form():
    try:
        data = request.get_json()
        print("Новая заявка:")
        print(f"  Имя: {data.get('name')}")
        print(f"  Телефон: {data.get('phone')}")
        print(f"  Email: {data.get('email')}")
        print("-" * 40)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Ошибка формы:", e)
        return jsonify({"status": "error"}), 500


def main():
    application.run(host='0.0.0.0', port='8100', debug=True)

if __name__ == '__main__':
    main()
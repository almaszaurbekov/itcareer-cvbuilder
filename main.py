import services.auth as auth
from flask import Flask
from datetime import timedelta
from services.config import app_secret
import services.cvbuild as cvbuild
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = app_secret
app.permanent_session_lifetime = timedelta(days=30)
CORS(app, supports_credentials=True)

@app.route('/register', methods=['POST'])
def register():
    return auth.register()

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/check_access', methods=['GET'])
def check_access():
    return auth.check_access()

@app.route('/logout', methods=['POST'])
def logout():
    return auth.logout()

@app.route('/upgrade_bullet_points', methods=['POST'])
def upgrade_bullet_points():
    return cvbuild.upgrade_bullet_points()

if __name__ == '__main__':
    app.run(debug=True)
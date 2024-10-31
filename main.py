import services.auth as auth
from flask import Flask
from datetime import timedelta
from services.config import app_secret
import services.cvbuild as cvbuild
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = app_secret
CORS(app, supports_credentials=True)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    return auth.register()

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/check_access', methods=['GET'])
@jwt_required()
def check_access():
    return auth.check_access()

@app.route('/upgrade_bullet_points', methods=['POST'])
@jwt_required()
def upgrade_bullet_points():
    return cvbuild.upgrade_bullet_points()

if __name__ == '__main__':
    app.run(debug=True)
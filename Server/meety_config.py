# Импорт модулей
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Flask etc
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
# app.config['DEBUG'] = False
app.config["JWT_SECRET_KEY"] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\Raid\\cp\\meety_test.db'
cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

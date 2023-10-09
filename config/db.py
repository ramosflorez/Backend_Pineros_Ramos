from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#creamos las credenciales para conectarnos a la bd
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:20023006@localhost/sistemacalzado'
app.config['SQLALCHEMY_TRACK_MODIFACATIONS'] = False

app.secret_key = "WebAvanzada"

#creamos los objetos de bd

db = SQLAlchemy(app)
ma = Marshmallow(app)
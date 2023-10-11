from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#creamos las credenciales para conectarnos a la bd
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sistemacalzado'
app.config['SQLALCHEMY_TRACK_MODIFACATIONS'] = False

app.secret_key = "WebAvanzada"

#creamos los objetos de bd y migración

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
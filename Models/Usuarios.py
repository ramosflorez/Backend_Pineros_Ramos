from config.db import ma, db, app

class Usuario(db.Model):
    __tablename__ = "tblusuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    rol = db.Column(db.String(20))

    def __init__(self, nombre, email, password, rol):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol

    #convertir una instancia del modelo Usuario en un diccionario
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'password', 'rol')

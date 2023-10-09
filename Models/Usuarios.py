from config.db import ma, db, app

class Usuario(db.Model):
    __tablename__ = "tblusuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    email = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    rol = db.Column(db.String(20))

    def __init__(self, id, nombre, email, contraseña, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.rol = rol

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'contraseña', 'rol')

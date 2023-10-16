from config.db import ma, db, app

class ContratacionUsuario(db.Model):
    __tablename__ = "tblcontratacion_usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tblusuario.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('tblproducto.id'))
    rol = db.Column(db.String(20))
    descripcion = db.Column(db.String(255))

    def __init__(self, id_usuario, id_producto, rol, descripcion):
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.rol = rol
        self.descripcion = descripcion

with app.app_context():
    db.create_all()

class ContratacionUsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_usuario', 'id_producto', 'rol', 'descripcion')
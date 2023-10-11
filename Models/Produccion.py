from config.db import ma, db, app

class Produccion(db.Model):
    __tablename__ = "tblproduccion"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tblusuario.id'))
    fecha = db.Column(db.DateTime)
    cantidad = db.Column(db.String(20))
    estado = db.Column(db.Boolean)
    total = db.Column(db.Float)

    def __init__(self, id, id_usuario, fecha, cantidad, estado, total):
        self.id = id
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.cantidad = cantidad
        self.estado = estado
        self.total = total

with app.app_context():
    db.create_all()

class ProduccionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_usuario','fecha', 'cantidad', 'estado', 'total')
from config.db import ma, db, app

class Produccion(db.Model):
    __tablename__ = "tblproduccion"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tblusuario.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('tblproducto.id'))
    fecha = db.Column(db.DateTime)
    cantidad = db.Column(db.String(20))
    total = db.Column(db.Float)

    def __init__(self, id, id_usuario, id_producto, fecha, cantidad, total):
        self.id = id
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.fecha = fecha
        self.cantidad = cantidad
        self.total = total

with app.app_context():
    db.create_all()

class ProduccionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_usuario', 'id_producto', 'fecha', 'cantidad', 'total')
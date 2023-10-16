from config.db import ma, db, app
import json 

class Detalle_Produccion(db.Model):
    __tablename__ = "tbldetalle_produccion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_produccion = db.Column(db.Integer, db.ForeignKey('tblproduccion.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('tblproducto.id'))
    nombre = db.Column(db.String(20))
    fecha = db.Column(db.DateTime)


    def __init__(self, id_produccion, id_producto, nombre, fecha):
        self.id_produccion = id_produccion
        self.id_producto = id_producto
        self.nombre = nombre
        self.fecha = fecha


with app.app_context():
    db.create_all()

class DetalleProduccionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'id_produccion', 'id_producto', 'fecha')
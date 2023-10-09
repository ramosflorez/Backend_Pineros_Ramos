from config.db import ma, db, app
import json 

class Paquete(db.Model):
    __tablename__ = "tblpaquete"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    produccion_productos = db.Column(db.JSON)
    fecha = db.Column(db.DateTime)
    compensacion = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, id, nombre, produccion_productos, fecha, compensacion, total):
        self.id = id
        self.nombre = nombre
        self.produccion_productos = produccion_productos
        self.fecha = fecha
        self.compensacion = compensacion
        self.total = total

with app.app_context():
    db.create_all()

class PaqueteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'produccion_productos', 'fecha', 'compensacion', 'total')
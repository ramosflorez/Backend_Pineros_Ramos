from config.db import ma, db, app

class Producto(db.Model):
    __tablename__ = "tblproducto"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float)
    rol = db.Column(db.String(20))

    def __init__(self, id, nombre, descripcion, precio, rol):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.rol = rol

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'precio', 'rol')
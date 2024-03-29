from config.db import ma, db, app

class Producto(db.Model):
    __tablename__ = "tblproducto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    rol = db.Column(db.String(20))
    precio = db.Column(db.Float)

    def __init__(self, nombre, descripcion, rol, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.rol = rol
        self.precio = precio

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'rol', 'precio')
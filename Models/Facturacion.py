from config.db import ma, db, app

class Facturacion(db.Model):
    __tablename__ = "tblfacturacion"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tblusuario.id'))
    id_produccion = db.Column(db.Integer, db.ForeignKey('tblproduccion.id'))
    id_paquete = db.Column(db.Integer, db.ForeignKey('tblpaquete.id'))
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Float)

    def __init__(self, id, id_usuario, id_produccion, id_paquete, fecha, monto_total):
        self.id = id
        self.id_usuario = id_usuario
        self.id_produccion = id_produccion
        self.id_paquete = id_paquete
        self.fecha = fecha
        self.monto_total = monto_total

with app.app_context():
    db.create_all()

class FacturacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_usuario', 'id_produccion', 'id_paquete', 'fecha', 'monto_total')
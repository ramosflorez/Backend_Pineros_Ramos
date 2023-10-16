from config.db import ma, db, app

class Facturacion(db.Model):
    __tablename__ = "tblfacturacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tblusuario.id'))
    produccion = db.Column(db.JSON)
    id_det_produccion = db.Column(db.Integer, db.ForeignKey('tbldetalle_produccion.id'))
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Float)

    def __init__(self,  id_usuario, produccion, id_det_produccion, fecha, monto_total):
        self.id_usuario = id_usuario
        self.produccion = produccion
        self.id_det_produccion = id_det_produccion
        self.fecha = fecha
        self.monto_total = monto_total

with app.app_context():
    db.create_all()

class FacturacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_usuario', 'produccion', 'id_det_produccion', 'fecha', 'monto_total')
from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Facturacion import Facturacion, FacturacionSchema

ruta_factura = Blueprint("routes_factura", __name__)

factura_schema   = FacturacionSchema()
facturas_schemas = FacturacionSchema(many=True)

@ruta_factura.route('/factura', methods=['GET', 'POST', 'DELETE'])
def factura():
    if request.method == 'GET':
        resultall = factura.query.all()
        resultFactura = facturas_schemas.dump(resultall)
        return jsonify(resultFactura)
    
    if request.method == 'POST':
        id = request.json['id']
        id_usuario = request.json['id_usuario']
        id_produccion = request.json['id_produccion']
        id_paquete = request.json['id_paquete']
        fecha = request.json['fecha']
        monto_total = request.json['monto_total']

        nuevo_factura = Facturacion(id=id, id_usuario=id_usuario, id_produccion=id_produccion, id_paquete=id_paquete, fecha=fecha, monto_total=monto_total)

        db.session.add(nuevo_factura)
        db.session.commit()

        return factura_schema.jsonify(nuevo_factura)
    
    if request.method == 'DELETE':
        id = request.json['id']
        factura = Facturacion.query.get(id)
        db.session.delete(factura)
        db.session.commit()
        return factura_schema.jsonify(factura)
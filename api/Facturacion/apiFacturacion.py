from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Facturacion import Facturacion, FacturacionSchema

ruta_factura = Blueprint("routes_factura", __name__)

factura_schema   = FacturacionSchema()
facturas_schemas = FacturacionSchema(many=True)

#ruta para obtener, crear y eliminar registros de facturas
@ruta_factura.route('/factura', methods=['GET', 'POST', 'DELETE'])
def factura():
    if request.method == 'GET':
        resultall = factura.query.all()
        resultFactura = facturas_schemas.dump(resultall)
        return jsonify(resultFactura)
    
    if request.method == 'POST':
        id = request.json['id']
        id_usuario = request.json['id_usuario']
        produccion = request.json['produccion']
        id_det_produccion = request.json['id_det_produccion']
        fecha = request.json['fecha']
        monto_total = request.json['monto_total']

        nuevo_factura = Facturacion(id=id, id_usuario=id_usuario, produccion=produccion, id_det_produccion=id_det_produccion, fecha=fecha, monto_total=monto_total)

        db.session.add(nuevo_factura)
        db.session.commit()

        return factura_schema.jsonify(nuevo_factura)
    
    if request.method == 'DELETE':
        id = request.json['id']
        factura = Facturacion.query.get(id)
        db.session.delete(factura)
        db.session.commit()
        return factura_schema.jsonify(factura)
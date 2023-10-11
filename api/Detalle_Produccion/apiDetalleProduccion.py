from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Detalle_Produccion import Detalle_Produccion, DetalleProduccionSchema

ruta_detproduccion = Blueprint("routes_detproduccion", __name__)

detproduccion_schema   = DetalleProduccionSchema()
detproducciones_schemas = DetalleProduccionSchema(many=True)

#ruta para obtener, crear y eliminar registros de la tabla detalle_produccion
@ruta_detproduccion.route('/detproduccion', methods=['GET', 'POST', 'DELETE'])
def detproduccion():
    if request.method == 'GET':
        resultall = Detalle_Produccion.query.all()
        resultDetProduccion = detproducciones_schemas.dump(resultall)
        return jsonify(resultDetProduccion)
    
    if request.method == 'POST':
        id = request.json['id']
        id_produccion = request.json['id_produccion']
        id_producto = request.json['id_producto']
        nombre = request.json['nombre']
        fecha = request.json['fecha']
        compensacion = request.json['compensacion']
        total = request.json['total']

        nuevo_detproduccion = Detalle_Produccion(id=id, id_produccion=id_produccion, id_producto=id_producto, nombre=nombre, fecha=fecha, compensacion=compensacion, total=total)

        db.session.add(nuevo_detproduccion)
        db.session.commit()

        return detproduccion_schema.jsonify(nuevo_detproduccion)
    
    if request.method == 'DELETE':
        id = request.json['id']
        detproduccion = Detalle_Produccion.query.get(id)
        db.session.delete(detproduccion)
        db.session.commit()
        return detproduccion_schema.jsonify(detproduccion)
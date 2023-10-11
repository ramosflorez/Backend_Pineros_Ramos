from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Produccion import Produccion, ProduccionSchema

ruta_produccion = Blueprint("routes_produccion", __name__)

produccion_schema   = ProduccionSchema()
producciones_schemas = ProduccionSchema(many=True)

#ruta para obtener, crear y eliminar registros de produccion
@ruta_produccion.route('/produccion', methods=['GET', 'POST', 'DELETE'])
def produccion():
    if request.method == 'GET':
        resultall = Produccion.query.all()
        resultProduccion = producciones_schemas.dump(resultall)
        return jsonify(resultProduccion)
    
    if request.method == 'POST':
        id = request.json['id']
        id_usuario = request.json['id_usuario']
        fecha = request.json['fecha']
        cantidad = request.json['cantidad']
        estado = request.json['estado']
        total = request.json['total']

        nuevo_produccion = Produccion(id=id, id_usuario=id_usuario, fecha=fecha, cantidad=cantidad, estado=estado, total=total)

        db.session.add(nuevo_produccion)
        db.session.commit()

        return produccion_schema.jsonify(nuevo_produccion)
    
    if request.method == 'DELETE':
        id = request.json['id']
        produccion = Produccion.query.get(id)
        db.session.delete(produccion)
        db.session.commit()
        return produccion_schema.jsonify(produccion)
from flask import Blueprint, redirect, request, jsonify, session, render_template
from api.Usuarios.apiUsuarios import token_required
from config.db import app, db, ma
from Models.Detalle_Produccion import Detalle_Produccion, DetalleProduccionSchema

ruta_detproduccion = Blueprint("routes_detproduccion", __name__)

detproduccion_schema   = DetalleProduccionSchema()
detproducciones_schemas = DetalleProduccionSchema(many=True)

#ruta para obtener, crear y eliminar registros de la tabla detalle_produccion
@ruta_detproduccion.route('/detproduccion', methods=['GET', 'POST', 'DELETE'])
@token_required
def detproduccion(current_user):
    if request.method == 'GET':
        resultall = Detalle_Produccion.query.all()
        resultDetProduccion = detproducciones_schemas.dump(resultall)
        return jsonify(resultDetProduccion)
    
    if request.method == 'DELETE':
        id = request.json['id']
        detproduccion = Detalle_Produccion.query.get(id)
        db.session.delete(detproduccion)
        db.session.commit()
        return detproduccion_schema.jsonify(detproduccion)
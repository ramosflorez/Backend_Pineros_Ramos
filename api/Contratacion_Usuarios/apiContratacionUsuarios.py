from flask import Blueprint, redirect, request, jsonify, session, render_template
from api.Usuarios.apiUsuarios import token_required
from config.db import app, db, ma
from Models.Contratacion_Usuarios import ContratacionUsuario, ContratacionUsuarioSchema

ruta_contratacion = Blueprint("routes_contratacion", __name__)

contratacion_schema   = ContratacionUsuarioSchema()
contrataciones_schemas = ContratacionUsuarioSchema(many=True)

#ruta para obtener, crear y eliminar registros de la tabla contratacion
@ruta_contratacion.route('/contratacion', methods=['GET', 'POST', 'DELETE'])
@token_required
def contratacion(current_user):
    if request.method == 'GET':
        resultall = ContratacionUsuario.query.all()
        resultContratacion = contrataciones_schemas.dump(resultall)
        return jsonify(resultContratacion)
    
    if request.method == 'POST':
        id_usuario = request.json['id_usuario']
        id_producto = request.json['id_producto']
        rol = request.json['rol']
        descripcion = request.json['descripcion']

        nuevo_contratacion = ContratacionUsuario(id_usuario=id_usuario, id_producto=id_producto, rol=rol, descripcion=descripcion)

        db.session.add(nuevo_contratacion)
        db.session.commit()

        return contratacion_schema.jsonify(nuevo_contratacion)
    
    if request.method == 'DELETE':
        id = request.json['id']
        contratacion = ContratacionUsuario.query.get(id)
        db.session.delete(contratacion)
        db.session.commit()
        return contratacion_schema.jsonify(contratacion)
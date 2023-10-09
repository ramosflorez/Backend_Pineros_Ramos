from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Usuarios import Usuario, UsuarioSchema

ruta_usuario = Blueprint("routes_usuario", __name__)

usuario_schema   = UsuarioSchema()
usuarios_schemas = UsuarioSchema(many=True)

@ruta_usuario.route('/usuarios', methods=['GET', 'POST', 'DELETE'])
def usuarios():
    if request.method == 'GET':
        resultall = Usuario.query.all()
        resultUsuarios = usuarios_schemas.dump(resultall)
        return jsonify(resultUsuarios)
    
    if request.method == 'POST':
        id = request.json['id']
        nombre = request.json['nombre']
        email = request.json['email']
        contraseña = request.json['contraseña']
        rol = request.json['rol']

        nuevo_usuario = Usuario(id=id, nombre=nombre, email=email, contraseña=contraseña, rol=rol)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return usuario_schema.jsonify(nuevo_usuario)
    
    if request.method == 'DELETE':
        id = request.json['id']
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return usuario_schema.jsonify(usuario)

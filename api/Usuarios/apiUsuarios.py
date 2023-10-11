from flask import Blueprint, redirect, request, jsonify, session, render_template
from flask_bcrypt import Bcrypt
from config.db import app, db, ma, bcrypt
from Models.Usuarios import Usuario, UsuarioSchema
from common.jwt_utils import jwt_token_generate         # Es se utiliza para generar tokens JWT

ruta_usuario = Blueprint("routes_usuario", __name__)
#ruta para autenticación
auth_bp = Blueprint('auth', __name__)

usuario_schema   = UsuarioSchema()
usuarios_schemas = UsuarioSchema(many=True)

#ruta para autenticación (login)
@auth_bp.route('/login/<id>', methods=['POST'])
def login(id):
    data = request.get_json()
    password = data.get('password')

    usuario = Usuario.query.filter_by(id=id).first()

    if usuario and bcrypt.check_password_hash(usuario.password, password):
        #print(usuario.to_dict())
        respuesta = jwt_token_generate(usuario.to_dict())
        return jsonify(respuesta)
    else:
        return jsonify(message='Credenciales incorrectas'), 401

#ruta para obtener, crear y eliminar usuarios
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
        password = request.json['password']
        rol = request.json['rol']

        #aplica la función de hashing (bcrypt) a la contraseña almacenada en la variable password
        password = bcrypt.generate_password_hash(password)

        nuevo_usuario = Usuario(id=id, nombre=nombre, email=email, password=password, rol=rol)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return usuario_schema.jsonify(nuevo_usuario)
    
    if request.method == 'DELETE':
        id = request.json['id']
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return usuario_schema.jsonify(usuario)

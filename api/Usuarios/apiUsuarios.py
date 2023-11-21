from functools import wraps
from flask import Blueprint, redirect, request, jsonify, session, render_template
from flask_bcrypt import Bcrypt
import jwt
from config.db import app, db, ma, bcrypt
from Models.Usuarios import Usuario, UsuarioSchema
from common.jwt_utils import jwt_token_generate, SECRET_KEY         # Es se utiliza para generar tokens JWT

ruta_usuario = Blueprint("routes_usuario", __name__)
#ruta para autenticación
auth_bp = Blueprint('auth', __name__)

usuario_schema   = UsuarioSchema()
usuarios_schemas = UsuarioSchema(many=True)

#decorador para validar token
def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token_admin = None

        if 'Authorization' in request.headers:
            token_admin = request.headers['Authorization'].split(" ")[1]

        if not token_admin:
            return jsonify({'message': 'Token de acceso faltante'}), 401

        try:
            data = jwt.decode(token_admin, SECRET_KEY, algorithms=['HS256'])
            current_user = Usuario.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token de acceso inválido'}), 401
        
        # Verifica si el rol del usuario es "administrador"
        if current_user.rol != "administrador":
            return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 401

        return func(current_user, *args, **kwargs)

    return decorated

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token de acceso faltante'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = Usuario.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token de acceso inválido'}), 401
        return func(current_user, *args, **kwargs)
    return decorated


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

#ruta para obtener y eliminar usuarios
@ruta_usuario.route('/usuarios', methods=['GET', 'DELETE'])
@admin_required
def usuarios(current_user):
    if request.method == 'GET':
        resultall = Usuario.query.all()
        resultUsuarios = usuarios_schemas.dump(resultall)
        return jsonify(resultUsuarios)
    
    if request.method == 'DELETE':
        id = request.json['id']
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return usuario_schema.jsonify(usuario)

# Ruta para acceder a la creación de usuarios sin validación de token
@ruta_usuario.route('/nuevousuario', methods=['POST'])
def crear_usuarios():

    nombre = request.json['nombre']
    email = request.json['email']
    password = request.json['password']
    rol = request.json['rol']

    #aplica la función de hashing (bcrypt) a la contraseña almacenada en la variable password
    password = bcrypt.generate_password_hash(password)

    nuevo_usuario = Usuario(nombre=nombre, email=email, password=password, rol=rol)
    result=usuario_schema.jsonify(nuevo_usuario)   

    db.session.add(nuevo_usuario)
    db.session.commit()

    return {
        "message": "User created",
        "user": result.__repr__()
    } 
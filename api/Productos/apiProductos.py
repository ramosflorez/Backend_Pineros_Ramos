from flask import Blueprint, redirect, request, jsonify, session, render_template
from api.Usuarios.apiUsuarios import admin_required
from config.db import app, db, ma
from Models.Productos import Producto, ProductoSchema
from common.jwt_utils import jwt_token_generate  

ruta_producto = Blueprint("routes_producto", __name__)

producto_schema   = ProductoSchema()
productos_schemas = ProductoSchema(many=True)

#ruta para obtener, crear y eliminar registros de productos
@ruta_producto.route('/productos', methods=['GET', 'POST', 'DELETE'])
@admin_required
def productos(current_user):
    if request.method == 'GET':
        resultall = Producto.query.all()
        resultProductos = productos_schemas.dump(resultall)
        return jsonify(resultProductos)
    
    if request.method == 'POST':
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']
        precio = request.json['precio']

        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio)
        result=producto_schema.jsonify(nuevo_producto)
        db.session.add(nuevo_producto)
        db.session.commit()

        return {
            "mensaje": "Producto creado",
            "producto": result.__repr__()
        } 
    
    if request.method == 'DELETE':
        id = request.json['id']
        producto = Producto.query.get(id)
        db.session.delete(producto)
        db.session.commit()
        return producto_schema.jsonify(producto)

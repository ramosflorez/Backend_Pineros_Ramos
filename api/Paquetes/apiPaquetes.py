from flask import Blueprint, redirect, request, jsonify, session, render_template
from config.db import app, db, ma
from Models.Paquetes import Paquete, PaqueteSchema

ruta_paquete = Blueprint("routes_paquete", __name__)

paquete_schema   = PaqueteSchema()
paquetes_schemas = PaqueteSchema(many=True)

@ruta_paquete.route('/paquete', methods=['GET', 'POST', 'DELETE'])
def paquete():
    if request.method == 'GET':
        resultall = Paquete.query.all()
        resultPaquete = paquetes_schemas.dump(resultall)
        return jsonify(resultPaquete)
    
    if request.method == 'POST':
        id = request.json['id']
        nombre = request.json['nombre']
        produccion_productos = request.json['produccion_productos']
        fecha = request.json['fecha']
        compensacion = request.json['compensacion']
        total = request.json['total']

        nuevo_paquete = Paquete(id=id, nombre=nombre, produccion_productos=produccion_productos, fecha=fecha, compensacion=compensacion, total=total)

        db.session.add(nuevo_paquete)
        db.session.commit()

        return paquete_schema.jsonify(nuevo_paquete)
    
    if request.method == 'DELETE':
        id = request.json['id']
        paquete = Paquete.query.get(id)
        db.session.delete(paquete)
        db.session.commit()
        return paquete_schema.jsonify(paquete)
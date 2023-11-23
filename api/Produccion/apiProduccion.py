import datetime
from flask import Blueprint, redirect, request, jsonify, session, render_template
from api.Usuarios.apiUsuarios import token_required
from config.db import app, db, ma
from Models.Produccion import Produccion, ProduccionSchema
from Models.Detalle_Produccion import Detalle_Produccion, DetalleProduccionSchema
from Models.Productos import Producto, ProductoSchema
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

ruta_produccion = Blueprint("routes_produccion", __name__)

produccion_schema   = ProduccionSchema()
producciones_schemas = ProduccionSchema(many=True)

detproduccion_schema   = DetalleProduccionSchema()
detproducciones_schemas = DetalleProduccionSchema(many=True)

producto_schema   = ProductoSchema()
productos_schemas = ProductoSchema(many=True)

#ruta para obtener, crear y eliminar registros de produccion
@ruta_produccion.route('/produccion', methods=['GET', 'POST', 'DELETE'])
@token_required
def produccion(current_user):
    try:
        if request.method == 'GET':
            resultall = Produccion.query.all()
            resultProduccion = producciones_schemas.dump(resultall)
            return jsonify(resultProduccion)
    
        if request.method == 'POST':
            
            id_usuario = request.json["produccion"]['id_usuario']
            fecha = date.today().isoformat()
            cantidad = request.json["produccion"]['cantidad']
            id_producto= request.json["detalle"]['id_producto']
            nombre =request.json["detalle"]['nombre']
            total=0.000


            print("holaaa", date.today().isoformat())
            
            # Calcular compensación
            compensacion= 0.12 if cantidad==12 else 0.00

            #obtener el precio por el producto individual
            producto=Producto.query.filter(Producto.id==id_producto).first()
            precio= producto.precio

            #obtener todas las producciones
            producciones=Produccion.query.filter((Produccion.estado == 0) & (Produccion.fecha == fecha)).all()

            if len(producciones)>0:
                for produccion in producciones:
                    detalle_produccion= Detalle_Produccion.query.filter(Detalle_Produccion.id_produccion == produccion.id).all()
                    if(detalle_produccion[0].id_producto==id_producto):
                        disponible=12-produccion.cantidad
                        if(disponible>0):
                            produccion.cantidad+= cantidad if cantidad<=disponible else disponible
                            for i in range (min(cantidad, disponible)):
                                cantidad-=1
                                disponible-=1
                                nuevo_detproduccion = Detalle_Produccion(id_produccion=produccion.id, id_producto=id_producto, nombre=nombre, fecha=fecha)
                                db.session.add(nuevo_detproduccion)
                                db.session.commit()

                            #actualizaciones de la tabla produccion
                            total=precio*produccion.cantidad
                            produccion.compensacion=compensacion
                            produccion.total=((total * compensacion) + total)
                            if(produccion.cantidad==12):
                                produccion.compensacion=0.12
                                produccion.estado=1

                            db.session.commit()
                            total=0.000

                            
            while cantidad>0:
                nuevo_produccion = Produccion(id_usuario=id_usuario, fecha=fecha, cantidad=cantidad if cantidad<=12 else 12, estado=1 if cantidad>=12 else 0, compensacion=compensacion,total=total)
                db.session.add(nuevo_produccion)
                db.session.commit()
                for i in range(min(cantidad,12)):
                    cantidad-=1
                    nuevo_detproduccion = Detalle_Produccion(id_produccion=nuevo_produccion.id, id_producto=id_producto, nombre=nombre, fecha=fecha)
                    db.session.add(nuevo_detproduccion)
                    db.session.commit()
                nuevo_produccion.total=((nuevo_produccion.cantidad * precio) * nuevo_produccion.compensacion) + (nuevo_produccion.cantidad * precio)
                db.session.commit()
                    
            return {"mensaje":"Produccion creada"}
    
    except SQLAlchemyError as e:
            # Log the error for debugging purposes
            print(f"SQLAlchemy Error: {str(e)}")

            # Devuelve un mensaje de error como JSON
            return jsonify({"error": "Error de base de datos"}), 500

    except Exception as e:
        # Log the general exception for debugging purposes
        print(f"An unexpected error occurred: {str(e)}")

        # Devuelve un mensaje de error como JSON
        return jsonify({"error": "Error inesperado"}), 500

# Ruta para eliminar producción y su detalle asociado
@ruta_produccion.route('/produccion', methods=['DELETE'])
@token_required
def delete_production_and_details(current_user):
    try:
        # Obtén el ID de la producción desde el cuerpo de la solicitud
        production_id = request.json['id']

        # Elimina los detalles de producción asociados a la producción
        Detalle_Produccion.query.filter_by(id_produccion=production_id).delete()

        # Luego, elimina la producción en sí
        produccion = Produccion.query.get(production_id)
        db.session.delete(produccion)
        db.session.commit()

        return produccion_schema.jsonify(produccion)

    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"SQLAlchemy Error: {str(e)}")

        # Devuelve un mensaje de error como JSON
        return jsonify({"error": "Error de base de datos"}), 500

    except Exception as e:
        # Log the general exception for debugging purposes
        print(f"An unexpected error occurred: {str(e)}")

        # Devuelve un mensaje de error como JSON
        return jsonify({"error": "Error inesperado"}), 500

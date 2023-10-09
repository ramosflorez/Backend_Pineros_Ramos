from flask import Flask, request, jsonify, redirect, render_template
from config.db import app
from api.Usuarios.apiUsuarios import ruta_usuario
from api.Productos.apiProductos import ruta_producto
from api.Produccion.apiProduccion import ruta_produccion
from api.Paquetes.apiPaquetes import ruta_paquete
from api.Facturacion.apiFacturacion import ruta_factura

app.register_blueprint(ruta_usuario, url_prefix = "/api" )
app.register_blueprint(ruta_producto, url_prefix = "/api")
app.register_blueprint(ruta_produccion, url_prefix = "/api")
app.register_blueprint(ruta_paquete, url_prefix = "/api")
app.register_blueprint(ruta_factura, url_prefix = "/api")

@app.route("/")
def index():
    return "Hola Mundo"

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
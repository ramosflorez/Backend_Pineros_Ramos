from flask import Flask, request, jsonify, redirect, render_template
from config.db import app
from api.Usuarios.apiUsuarios import ruta_usuario, auth_bp
from api.Productos.apiProductos import ruta_producto
from api.Produccion.apiProduccion import ruta_produccion
from api.Detalle_Produccion.apiDetalleProduccion import ruta_detproduccion
from api.Facturacion.apiFacturacion import ruta_factura
from api.Contratacion_Usuarios.apiContratacionUsuarios import ruta_contratacion

app.register_blueprint(ruta_usuario)
app.register_blueprint(auth_bp)
app.register_blueprint(ruta_producto)
app.register_blueprint(ruta_produccion)
app.register_blueprint(ruta_detproduccion)
app.register_blueprint(ruta_factura)
app.register_blueprint(ruta_contratacion)


@app.route("/")
def index():
    return "Hola Mundo"

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
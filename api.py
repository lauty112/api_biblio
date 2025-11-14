import os
from flask import Flask, jsonify
from flask_cors import CORS
from conexion import obtener_conexion, desconectar
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
# Habilitar CORS para todas las rutas (configurable mediante env si se desea)
CORS(app)


@app.route('/api/libros', methods=['GET'])
def obtener_libros():
    """Devuelve la lista de libros desde la tabla `titulos`.

    Responde con JSON y código HTTP adecuado si hay error de conexión.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "no se puede conectar a la base de datos"}), 500

    try:
        # Usar context manager para asegurar cierre de cursor
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM titulos")
            libros = cursor.fetchall()
    except Exception as e:
        # Registrar el error en el servidor y devolver 500 al cliente
        print("Error consultando libros:", e)
        return jsonify({"error": "error al obtener los libros"}), 500
    finally:
        desconectar(conexion)

    return jsonify(libros)


if __name__ == '__main__':
    # Configuración del puerto y debug vía variables de entorno
    port = int(os.environ.get('PORT', 5000))
    debug_env = os.environ.get('FLASK_DEBUG', 'True').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug_env)



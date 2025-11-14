import os
from flask import Flask, jsonify
from flask_cors import CORS
from conexion import obtener_conexion, desconectar
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
# Habilitar CORS para todas las rutas (configurable mediante env si se desea)
CORS(app)

@app.route('/')
def home():
    return "API de Biblioteca funcionando"

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
@app.route('/api/autores', methods=['DELETE'])
def eliminar_autores():
    """Elimina todos los autores de la tabla `autores`.

    Responde con JSON y código HTTP adecuado si hay error de conexión.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "no se puede conectar a la base de datos"}), 500

    try:
        # Usar context manager para asegurar cierre de cursor
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM autores")
            conexion.commit()
            afectados = cursor.rowcount
    except Exception as e:
        # Registrar el error en el servidor y devolver 500 al cliente
        print("Error eliminando autores:", e)
        return jsonify({"error": "error al eliminar los autores"}), 500
    finally:
        desconectar(conexion)

    return jsonify({"mensaje": f"{afectados} autores eliminados"}), 200
@app.route('/api/autores', methods=['POST'])
def agregar_autor():
    """Agrega un nuevo autor a la tabla `autores`.

    Responde con JSON y código HTTP adecuado si hay error de conexión.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "no se puede conectar a la base de datos"}), 500

    try:
        # Usar context manager para asegurar cierre de cursor
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO autores (nombre,autor_id) VALUES ('cortaza', '1')")
            conexion.commit()
            afectados = cursor.rowcount
    except Exception as e:
        # Registrar el error en el servidor y devolver 500 al cliente
        print("Error agregando autor:", e)
        return jsonify({"error": "error al agregar el autor"}), 500
    finally:
        desconectar(conexion)

    return jsonify({"mensaje": f"{afectados} autor agregado"}), 201
@app.route('/api/autores', methods=['PUT'])
def actualizar_autores():
    """Devuelve la lista de autores desde la tabla `autores`.

    Responde con JSON y código HTTP adecuado si hay error de conexión.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "no se puede conectar a la base de datos"}), 500

    try:
        # Usar context manager para asegurar cierre de cursor
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM autores")
            autores = cursor.fetchall()
    except Exception as e:
        # Registrar el error en el servidor y devolver 500 al cliente
        print("Error consultando autores:", e)
        return jsonify({"error": "error al obtener los autores"}), 500
    finally:
        desconectar(conexion)

    return jsonify(autores)
@app.route('/api/autores', methods=['GET'])
def obtener_autores():
    """Devuelve la lista de autores desde la tabla `autores`.

    Responde con JSON y código HTTP adecuado si hay error de conexión.
    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": "no se puede conectar a la base de datos"}), 500

    try:
        # Usar context manager para asegurar cierre de cursor
        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM autores")
            autores = cursor.fetchall()
    except Exception as e:
        # Registrar el error en el servidor y devolver 500 al cliente
        print("Error consultando autores:", e)
        return jsonify({"error": "error al obtener los autores"}), 500
    finally:
        desconectar(conexion)

    return jsonify(autores)


if __name__ == '__main__':
    # Configuración del puerto y debug vía variables de entorno
    port = int(os.environ.get('PORT', 5000))
    debug_env = os.environ.get('FLASK_DEBUG', 'True').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug_env)



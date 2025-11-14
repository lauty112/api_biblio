import os
import psycopg2


def obtener_conexion():
    """Crear y devolver una conexión a PostgreSQL.

    Lee la configuración desde variables de entorno y usa valores por
    defecto razonables para desarrollo local.
    Devuelve una conexión o None si falla.
    """
    try:
        conexion = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", 5432)),
            database=os.environ.get("DB_NAME", "biblioteca25"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "46315468")
        )

        print("Conexión exitosa a PostgreSQL")
        return conexion

    except Exception as e:
        # Registrar el error sin exponer secretos
        print("Error al conectar a la base de datos:", e)
        return None


def desconectar(conexion):
    """Cerrar la conexión si existe y devolver None."""
    if conexion:
        try:
            conexion.close()
            print("Conexión cerrada")
        except Exception as e:
            print("Error cerrando la conexión:", e)
    return None


if __name__ == "__main__":
    # Prueba rápida local
    conn = obtener_conexion()
    conn = desconectar(conn)

    

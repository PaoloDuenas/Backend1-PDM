from flask import Blueprint, request, jsonify
from config.db import mysql
import MySQLdb.cursors

tareas_bp = Blueprint("tareas", __name__)

# Función para obtener cursor


def get_db(dictionary=False):
    cursor = mysql.connection.cursor(
        MySQLdb.cursors.DictCursor if dictionary else None)
    return cursor


@tareas_bp.route("/obtener", methods=["GET"])
def obtener_tareas():
    cursor = get_db(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        return jsonify(tareas)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        cursor.close()


@tareas_bp.route("/crear", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"Error": "Debes enviar una descripcion"}), 400

    cursor = get_db()
    try:
        cursor.execute(
            "INSERT INTO tareas (descripcion) VALUES (%s)", (descripcion,))
        mysql.connection.commit()
        return jsonify({"message": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"}), 500
    finally:
        cursor.close()


@tareas_bp.route("/modificar/<int:id_tarea>", methods=["PUT"])
def modificar_tarea(id_tarea):
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"Error": "Debes enviar una descripcion"}), 400

    cursor = get_db()
    try:
        cursor.execute(
            "UPDATE tareas SET descripcion=%s, modificado_en=NOW() WHERE id_tarea=%s",
            (descripcion, id_tarea)
        )
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"Error": "No se encontró la tarea"}), 404
        return jsonify({"message": "Tarea modificada"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        cursor.close()


@tareas_bp.route("/eliminar/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    cursor = get_db()
    try:
        cursor.execute("DELETE FROM tareas WHERE id_tarea=%s", (id_tarea,))
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"Error": "No se encontró la tarea"}), 404
        return jsonify({"message": "Tarea eliminada"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        cursor.close()

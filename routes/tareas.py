from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.db import mysql
import MySQLdb.cursors

tareas_bp = Blueprint("tareas", __name__)


def get_db(dictionary=False):
    cursor = mysql.connection.cursor(
        MySQLdb.cursors.DictCursor if dictionary else None)
    return cursor


@tareas_bp.route("/obtener", methods=["GET"])
@jwt_required()
def obtener_tareas():
    id_usuarios = get_jwt_identity()
    try:
        cursor = get_db(dictionary=True)
        with cursor:
           
            cursor.execute(
                "SELECT * FROM tareas WHERE id_usuarios = %s", (id_usuarios,))
            tareas = cursor.fetchall()
        return jsonify(tareas)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@tareas_bp.route("/crear", methods=["POST"])
@jwt_required()
def crear_tarea():
    id_usuarios = get_jwt_identity()
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"Error": "Debes enviar una descripcion"}), 400

    try:
        cursor = get_db()
        with cursor:
            cursor.execute(
                "INSERT INTO tareas (descripcion, id_usuarios) VALUES (%s, %s)",
                (descripcion, id_usuarios)
            )
            mysql.connection.commit()
        return jsonify({"message": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"}), 500


@tareas_bp.route("/modificar/<int:id_tarea>", methods=["PUT"])
@jwt_required()
def modificar_tarea(id_tarea):
    id_usuarios = get_jwt_identity()
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"Error": "Debes enviar una descripcion"}), 400

    try:
        cursor = get_db()
        with cursor:
            cursor.execute(
                "UPDATE tareas SET descripcion=%s, modificado_en=NOW() WHERE id_tarea=%s AND id_usuarios=%s",
                (descripcion, id_tarea, id_usuarios)
            )
            mysql.connection.commit()
            if cursor.rowcount == 0:
                return jsonify({"Error": "No se encontró la tarea o no tienes permiso para modificarla"}), 404
        return jsonify({"message": "Tarea modificada"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@tareas_bp.route("/eliminar/<int:id_tarea>", methods=["DELETE"])
@jwt_required()
def eliminar_tarea(id_tarea):
    id_usuarios = get_jwt_identity()
    try:
        cursor = get_db()
        with cursor:
            cursor.execute(
                "DELETE FROM tareas WHERE id_tarea=%s AND id_usuarios=%s", (id_tarea, id_usuarios))
            mysql.connection.commit()
            if cursor.rowcount == 0:
                return jsonify({"Error": "No se encontró la tarea o no tienes permiso para eliminarla"}), 404
        return jsonify({"message": "Tarea eliminada"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

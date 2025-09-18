from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from config.db import get_db_connection
import datetime

usuarios_bp = Blueprint("usuarios", __name__)
bcrypt = Bcrypt()


@usuarios_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = None
    cursor = None
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Ese usuario ya existe"}), 400

        hashed_password = bcrypt.generate_password_hash(
            password).decode("utf-8")
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hashed_password)
        )
        conn.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"No se pudo crear el usuario: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()


@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = None
    try:
        conn, cursor = get_db_connection(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario or not bcrypt.check_password_hash(usuario["password"], password):
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # Generar token JWT (expira en 1 hora)
        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(
            identity=usuario["id"], expires_delta=expires)

        return jsonify({
            "mensaje": "Login exitoso",
            "access_token": access_token,
            "usuario": {"id": usuario["id"], "nombre": usuario["nombre"], "email": usuario["email"]}
        }), 200

    except Exception as e:
        return jsonify({"error": f"No se pudo iniciar sesión: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
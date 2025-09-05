from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db, mysql

#importamos la ruta del blueprint
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

#load enviroment variables
load_dotenv()

def create_app(): # <--- funcion para crear la app
    #instancia de la app
    app=Flask(__name__)

    #configurar la db
    init_db(app)
    #registrar el blueprint
    app.register_blueprint(tareas_bp, url_prefix= '/tareas')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')


    return app


app= create_app() # creando la app

if __name__== "__main__":

    #Obtenemos el puerto
    port = int(os.getenv("PORT",8080))

    #corremos la app
    app.run(host="0.0.0.0", port=port, debug=True)
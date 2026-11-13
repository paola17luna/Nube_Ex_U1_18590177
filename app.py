import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

from sqlalchemy.engine import URL

password_file = os.getenv("POSTGRES_PASSWORD_FILE")

if password_file:
    with open(password_file, "r", encoding="utf-8") as archivo:
        password = archivo.read().strip()

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("POSTGRES_USER", "paola"),
        password=password,
        host=os.getenv("POSTGRES_HOST", "paola_postgres"),
        port=5432,
        database=os.getenv("POSTGRES_DB", "paola_db")
    )

else:
    database_url = os.getenv("DATABASE_URL") or "sqlite:///:memory:"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Hola Mundo - Examen U3 - 18590177"


@app.route("/health")
def health():
    try:
        with db.engine.connect() as conexion:
            conexion.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "connected",
            "message": "Flask conectado a PostgreSQL"
        }), 200

    except Exception:
        app.logger.exception("Error de conexion a la base de datos")
        return jsonify({
            "status": "error",
            "database": "disconnected"
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

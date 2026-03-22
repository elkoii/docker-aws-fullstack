from flask import Flask
import psycopg2
import socket
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "mydb"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )

@app.route("/")
def home():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Crear tabla si no existe
        cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
        conn.commit()

        # Obtener visitas
        cur.execute("SELECT count FROM visits;")
        result = cur.fetchone()

        if result is None:
            cur.execute("INSERT INTO visits (count) VALUES (1);")
            conn.commit()
            count = 1
        else:
            count = result[0] + 1
            cur.execute("UPDATE visits SET count = %s;", (count,))
            conn.commit()

        cur.close()
        conn.close()

        hostname = socket.gethostname()

        return f"Servidor: {hostname} | Visitas: {count}"

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

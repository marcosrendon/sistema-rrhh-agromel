from flask import Flask, request
import sqlite3
import qrcode
import socket

app = Flask(__name__)

# Crear base de datos
def init_db():
    conn = sqlite3.connect("rrhh.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS postulantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        cargo TEXT,
        experiencia INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def formulario():
    return """
    <h2>Formulario de Postulación</h2>
    <form method='POST' action='/guardar'>
        Nombre:<br>
        <input name='nombre' required><br><br>

        Cargo:<br>
        <input name='cargo' required><br><br>

        Años de experiencia:<br>
        <input name='experiencia' type='number' required><br><br>

        <button type='submit'>Enviar</button>
    </form>
    """

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    cargo = request.form["cargo"]
    experiencia = int(request.form["experiencia"])

    conn = sqlite3.connect("rrhh.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO postulantes (nombre, cargo, experiencia) VALUES (?, ?, ?)",
        (nombre, cargo, experiencia)
    )
    conn.commit()
    conn.close()

    return "Postulación enviada correctamente ✅"

@app.route("/admin")
def admin():
    conn = sqlite3.connect("rrhh.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM postulantes ORDER BY experiencia DESC")
    datos = cursor.fetchall()
    conn.close()

    resultado = "<h2>Postulantes (ordenados por experiencia)</h2>"
    for d in datos:
        resultado += f"<p>ID: {d[0]} | Nombre: {d[1]} | Cargo: {d[2]} | Experiencia: {d[3]} años</p>"

    return resultado

if __name__ == "__main__":
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    url = f"http://{ip}:5000"

    # Generar QR
    img = qrcode.make(url)
    img.save("qr_postulacion.png")

    print("=================================")
    print("Escanea el QR para postular:")
    print(url)
    print("Panel administrador:")
    print(url + "/admin")
    print("=================================")

    app.run(host="0.0.0.0", port=5000)
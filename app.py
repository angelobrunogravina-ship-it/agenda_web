# app.py

from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DB = os.path.join(os.path.dirname(__file__), "agenda.db")

TIPI = [
    "Ferie",
    "Ferie a.s. Precedente",
    "Legge 104",
    "Malattia",
    "Smart Working",
    "Altro"
]


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():

    c = conn()

    c.execute("""
        CREATE TABLE IF NOT EXISTS eventi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            data_inizio TEXT,
            data_fine TEXT,
            giorni INTEGER,
            descrizione TEXT
        )
    """)

    c.commit()
    c.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/eventi")
def eventi():

    c = conn()

    rows = c.execute("""
        SELECT *
        FROM eventi
        ORDER BY date(data_inizio) DESC
    """).fetchall()

    c.close()

    return jsonify([dict(r) for r in rows])


@app.route("/totali")
def totali():

    c = conn()

    risultati = {}

    for tipo in TIPI:

        row = c.execute("""
            SELECT COALESCE(SUM(giorni), 0)
            FROM eventi
            WHERE tipo=?
        """, (tipo,)).fetchone()

        risultati[tipo] = row[0]

    c.close()

    return jsonify(risultati)


@app.route("/aggiungi", methods=["POST"])
def aggiungi():

    d = request.json

    d1 = datetime.fromisoformat(d["data_inizio"])
    d2 = datetime.fromisoformat(d["data_fine"])

    if d2 < d1:
        return {"errore": "Date non valide"}, 400

    giorni = (d2 - d1).days + 1

    c = conn()

    c.execute("""
        INSERT INTO eventi(
            tipo,
            data_inizio,
            data_fine,
            giorni,
            descrizione
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        d["tipo"],
        d["data_inizio"],
        d["data_fine"],
        giorni,
        d.get("descrizione", "")
    ))

    c.commit()
    c.close()

    return {"ok": True}


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    d = request.json

    d1 = datetime.fromisoformat(d["data_inizio"])
    d2 = datetime.fromisoformat(d["data_fine"])

    if d2 < d1:
        return {"errore": "Date non valide"}, 400

    giorni = (d2 - d1).days + 1

    c = conn()

    c.execute("""
        UPDATE eventi
        SET
            tipo=?,
            data_inizio=?,
            data_fine=?,
            giorni=?,
            descrizione=?
        WHERE id=?
    """, (
        d["tipo"],
        d["data_inizio"],
        d["data_fine"],
        giorni,
        d.get("descrizione", ""),
        id
    ))

    c.commit()
    c.close()

    return {"ok": True}


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    c = conn()

    c.execute("""
        DELETE FROM eventi
        WHERE id=?
    """, (id,))

    c.commit()
    c.close()

    return {"ok": True}


if __name__ == "__main__":

    init_db()

    app.run(debug=True)

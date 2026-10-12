from datetime import datetime, timezone
from threading import Lock

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
lock = Lock()
waiting = []
desks = {i: {"number": i, "status": "disponible", "current": None, "next": None} for i in range(1, 5)}
completed = 0
sequence = 0


def snapshot():
    return {"waiting": list(waiting), "desks": [dict(d) for d in desks.values()], "stats": {"atendidos": completed, "enEspera": len(waiting), "ventanillasDisponibles": sum(d["status"] == "disponible" for d in desks.values())}}


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "turnos-flask"})


@app.get("/api/state")
def state():
    with lock:
        return jsonify(snapshot())


@app.post("/api/turns")
def create_turn():
    global sequence
    with lock:
        sequence += 1
        turn = {"id": sequence, "folio": f"A{sequence:02d}", "created_at": datetime.now(timezone.utc).isoformat()}
        waiting.append(turn)
        return jsonify(turn), 201


@app.post("/api/desks/<int:number>/call")
def call_turn(number):
    with lock:
        desk = desks.get(number)
        if desk is None:
            return jsonify({"error": "Ventanilla inválida"}), 404
        if desk["status"] == "ocupada":
            return jsonify({"error": "La ventanilla está ocupada"}), 409
        if not waiting:
            return jsonify({"error": "No hay turnos en espera"}), 409
        desk["current"] = waiting.pop(0)
        desk["status"] = "ocupada"
        return jsonify({"folio": desk["current"]["folio"], "desk": number, "state": snapshot()})


@app.post("/api/desks/<int:number>/finish")
def finish_turn(number):
    global completed
    with lock:
        desk = desks.get(number)
        if desk is None:
            return jsonify({"error": "Ventanilla inválida"}), 404
        if desk["status"] != "ocupada":
            return jsonify({"error": "La ventanilla ya está disponible"}), 409
        completed += 1
        desk["status"] = "disponible"
        desk["current"] = None
        next_turn = waiting[0] if waiting else None
        desk["next"] = next_turn
        return jsonify({"folio": next_turn["folio"] if next_turn else None, "desk": number, "state": snapshot()})

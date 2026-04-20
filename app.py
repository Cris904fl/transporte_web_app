"""
Problema de Transporte de Grano — Colombia → Europa del Este
Aplicación web interactiva con Flask
Ejecutar: python app.py
Abrir:    http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import os

app = Flask(__name__)


# ─── MÉTODO DE VOGEL ────────────────────────────────────────────────────────
def metodo_vogel(oferta, demanda, costos):
    m, n = len(oferta), len(demanda)
    s = list(map(float, oferta))
    d = list(map(float, demanda))
    c = [list(map(float, row)) for row in costos]
    alloc = [[0.0] * n for _ in range(m)]
    fila_listo = [False] * m
    col_lista  = [False] * n
    pasos = []

    def pen_fila(i):
        vals = sorted(c[i][j] for j in range(n) if not col_lista[j])
        return round(vals[1] - vals[0], 2) if len(vals) >= 2 else (vals[0] if vals else -1)

    def pen_col(j):
        vals = sorted(c[i][j] for i in range(m) if not fila_listo[i])
        return round(vals[1] - vals[0], 2) if len(vals) >= 2 else (vals[0] if vals else -1)

    iteracion = 1
    while not all(fila_listo) and not all(col_lista):
        pf = [pen_fila(i) if not fila_listo[i] else -1 for i in range(m)]
        pc = [pen_col(j)  if not col_lista[j]  else -1 for j in range(n)]
        max_pf, max_pc = max(pf), max(pc)

        if max_pf >= max_pc:
            i = pf.index(max_pf)
            j = min((j for j in range(n) if not col_lista[j]), key=lambda j: c[i][j])
            tipo, pen = f"fila", max_pf
        else:
            j = pc.index(max_pc)
            i = min((i for i in range(m) if not fila_listo[i]), key=lambda i: c[i][j])
            tipo, pen = f"columna", max_pc

        qty = min(s[i], d[j])
        alloc[i][j] += qty
        s[i] -= qty
        d[j] -= qty

        pasos.append({
            "num": iteracion,
            "origen_idx": i,
            "destino_idx": j,
            "cantidad": int(qty),
            "costo_unit": c[i][j],
            "penalizacion": pen,
            "tipo": tipo
        })

        if s[i] < 0.001: fila_listo[i] = True
        if d[j] < 0.001: col_lista[j] = True
        iteracion += 1

    costo_total = sum(alloc[i][j] * costos[i][j]
                      for i in range(m) for j in range(n))
    return alloc, costo_total, pasos


# ─── DISTRIBUCIÓN POR ESCASEZ ───────────────────────────────────────────────
def distribuir_escasez(demanda, costos, disponible, criterio):
    n = len(demanda)
    alloc = [0] * n
    rem = float(disponible)

    if criterio == "proporcional":
        ratio = disponible / sum(demanda)
        alloc = [round(d * ratio) for d in demanda]

    elif criterio == "min_costo":
        prom = [sum(costos[i][j] for i in range(len(costos))) / len(costos)
                for j in range(n)]
        orden = sorted(range(n), key=lambda j: prom[j])
        for j in orden:
            qty = min(demanda[j], rem)
            alloc[j] = int(qty)
            rem -= qty

    elif criterio == "urgencia":
        for j in range(n):
            qty = min(demanda[j], rem)
            alloc[j] = int(qty)
            rem -= qty

    return alloc


# ─── RUTAS ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resolver", methods=["POST"])
def resolver():
    data = request.json
    origenes  = data["origenes"]
    destinos  = data["destinos"]
    oferta    = list(map(float, data["oferta"]))
    demanda   = list(map(float, data["demanda"]))
    costos    = [[float(v) for v in row] for row in data["costos"]]

    alloc, costo_total, pasos = metodo_vogel(oferta, demanda, costos)

    rutas = []
    for i, orig in enumerate(origenes):
        for j, dest in enumerate(destinos):
            if alloc[i][j] > 0:
                rutas.append({
                    "origen": orig, "destino": dest,
                    "origen_idx": i, "destino_idx": j,
                    "cantidad": int(alloc[i][j]),
                    "costo_unit": costos[i][j],
                    "costo_total": int(alloc[i][j] * costos[i][j])
                })

    cobertura = []
    for j, dest in enumerate(destinos):
        rec = sum(alloc[i][j] for i in range(len(origenes)))
        cobertura.append({
            "destino": dest,
            "demanda": int(demanda[j]),
            "recibe": int(rec),
            "ok": rec >= demanda[j]
        })

    return jsonify({
        "rutas": rutas,
        "costo_total": int(costo_total),
        "pasos": pasos,
        "alloc": [[int(v) for v in row] for row in alloc],
        "cobertura": cobertura
    })


@app.route("/escasez", methods=["POST"])
def escasez():
    data = request.json
    demanda    = list(map(float, data["demanda"]))
    costos     = [[float(v) for v in row] for row in data["costos"]]
    disponible = float(data["disponible"])
    criterio   = data["criterio"]
    destinos   = data["destinos"]

    alloc = distribuir_escasez(demanda, costos, disponible, criterio)
    total_dem = sum(demanda)

    resultado = []
    for j, dest in enumerate(destinos):
        pct = round(alloc[j] / demanda[j] * 100) if demanda[j] > 0 else 0
        resultado.append({
            "destino": dest,
            "demanda": int(demanda[j]),
            "recibe": alloc[j],
            "deficit": int(demanda[j]) - alloc[j],
            "pct": pct
        })

    return jsonify({
        "resultado": resultado,
        "disponible": int(disponible),
        "total_demanda": int(total_dem),
        "deficit_total": int(total_dem - disponible),
        "cobertura_pct": round(disponible / total_dem * 100)
    })


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🌾 Problema de Transporte de Grano")
    print("  Abre en tu navegador: http://localhost:5000")
    print("="*50 + "\n")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
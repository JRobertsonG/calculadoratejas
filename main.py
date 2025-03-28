from collections import Counter
from flask import Flask, render_template, request
from itertools import product
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        ancho = float(request.form["ancho"])
        largo = float(request.form["largo"])
        tipo_teja = request.form["tipo_teja"]

        tejas_base = [
            {"id": 4, "largo_util": 1.07, "ancho_util": 0.82},
            {"id": 5, "largo_util": 1.37, "ancho_util": 0.82},
            {"id": 6, "largo_util": 1.68, "ancho_util": 0.82},
            {"id": 8, "largo_util": 2.29, "ancho_util": 0.82},
            {"id": 10, "largo_util": 2.90, "ancho_util": 0.82}
        ]

        if tipo_teja == "opcion2":
            tejas_base.append({"id": 12, "largo_util": 3.51, "ancho_util": 0.82})

        tejas = tejas_base
        tejas_por_fila = math.ceil(ancho / 0.82)
        combinaciones = []

        for r in range(1, 10):
            for combo in product(tejas, repeat=r):
                suma_largo = sum(t["largo_util"] for t in combo)
                if suma_largo > largo + 0.7:
                    continue
                if suma_largo >= largo:
                    combinaciones.append({
                        "combo": [t["id"] for t in combo],
                        "largo_total": round(suma_largo, 2),
                        "tejas_por_fila": tejas_por_fila,
                        "total_tejas": tejas_por_fila * len(combo)
                    })

        if combinaciones:
            combinaciones.sort(key=lambda x: x["total_tejas"])
            resultado = combinaciones[0]
            conteo = Counter(resultado["combo"])
            detalle_tejas = []
            for tipo, cantidad in conteo.items():
                total = cantidad * resultado["tejas_por_fila"]
                detalle_tejas.append({"tipo": tipo, "cantidad": total})
            resultado["detalle_tejas"] = detalle_tejas
        else:
            resultado = {
                "combo": [],
                "largo_total": 0,
                "tejas_por_fila": 0,
                "total_tejas": 0,
                "detalle_tejas": []
            }

    return render_template("index.html", resultado=resultado)
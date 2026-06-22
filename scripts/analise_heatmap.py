"""
Processa heatmaps do SofaScore e calcula similaridade posicional com Raphinha.

Input: data/raw/heatmap_{player}.json  (retorno bruto da API SofaScore)
Output: imprime zone vectors + cosine similarity, atualiza ajuste_tatico no CSV

Convenção de coordenadas SofaScore:
  x: 0 → 100  (gol proprio → gol adversario)
  y: 0 → 100  (largura do campo)
  Artefato conhecido: x>=98, y<=1 (canto de escanteio) — filtrado

Zonas (3x3 grid):
  Profundidade: defensivo(x<33) | meio(33<=x<67) | ataque(x>=67)
  Largura:      esq(y<30)       | centro(30<=y<=70) | dir(y>70)
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"

PLAYERS = {
    "raphinha":      "Raphinha",
    "rayan":         "Rayan",
    "endrick":       "Endrick",
    "luiz_henrique": "Luiz Henrique",
}


def classify(x, y):
    zona_x = "defensivo" if x < 33 else ("meio" if x < 67 else "ataque")
    zona_y = "esq" if y < 30 else ("centro" if y <= 70 else "dir")
    return zona_x, zona_y


ZONE_KEYS = [
    ("defensivo", "esq"), ("defensivo", "centro"), ("defensivo", "dir"),
    ("meio",      "esq"), ("meio",      "centro"), ("meio",      "dir"),
    ("ataque",    "esq"), ("ataque",    "centro"), ("ataque",    "dir"),
]


def build_zone_vector(heatmap_path: Path) -> np.ndarray | None:
    if not heatmap_path.exists():
        return None

    with open(heatmap_path) as f:
        data = json.load(f)

    # Suporte a dois formatos: {"points": [...]} ou lista direta
    points = data.get("points", data) if isinstance(data, dict) else data

    counts = {k: 0 for k in ZONE_KEYS}
    total = 0

    for p in points:
        x, y, count = p.get("x", 0), p.get("y", 0), p.get("count", 1)

        # Filtra artefato do canto de escanteio
        if x >= 98 and y <= 1:
            continue

        zona = classify(x, y)
        counts[zona] = counts.get(zona, 0) + count
        total += count

    if total == 0:
        return None

    vec = np.array([counts[k] / total for k in ZONE_KEYS])
    return vec


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(np.dot(a, b) / norm)


def print_zone_table(name: str, vec: np.ndarray):
    labels_x = ["Defensivo", "Meio", "Ataque"]
    labels_y = ["Esq", "Centro", "Dir"]
    print(f"\n  {name}")
    print(f"  {'':12} {'Esq':>7} {'Centro':>7} {'Dir':>7}")
    for i, lx in enumerate(labels_x):
        row = [f"{vec[i*3+j]*100:6.1f}%" for j in range(3)]
        print(f"  {lx:12} {row[0]:>7} {row[1]:>7} {row[2]:>7}")


def main():
    print("=" * 60)
    print("ANALISE DE HEATMAP — SIMILARIDADE POSICIONAL COM RAPHINHA")
    print("=" * 60)

    vectors = {}
    for slug, name in PLAYERS.items():
        path = RAW_DIR / f"heatmap_{slug}.json"
        vec = build_zone_vector(path)
        if vec is None:
            print(f"\n[AVISO] {name}: arquivo {path} nao encontrado ou vazio")
        else:
            vectors[name] = vec
            print_zone_table(name, vec)

    if "Raphinha" not in vectors:
        print("\n[ERRO] Heatmap do Raphinha nao encontrado — nao eh possivel calcular similaridade.")
        return

    print("\n" + "=" * 60)
    print("SIMILARIDADE COSENO vs RAPHINHA (0-10)")
    print("=" * 60)

    ref = vectors["Raphinha"]
    scores = {}
    for name, vec in vectors.items():
        if name == "Raphinha":
            continue
        sim = cosine_similarity(ref, vec)
        score = round(sim * 10, 2)
        scores[name] = score
        print(f"  {name:20} {sim:.4f}  →  ajuste_tatico = {score}")

    # Atualiza CSV
    csv_path = DATA_DIR / "dataset_substituto_raphinha.csv"
    if csv_path.exists() and scores:
        df = pd.read_csv(csv_path)
        df["ajuste_tatico"] = df["ajuste_tatico"].astype(float)
        for name, score in scores.items():
            df.loc[df["player"] == name, "ajuste_tatico"] = score
        df.to_csv(csv_path, index=False)
        print(f"\nCSV atualizado: {csv_path}")

    print()


if __name__ == "__main__":
    main()

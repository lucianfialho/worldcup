"""
Monta o dataset final para o estudo de substituicao de Raphinha.
Usa dados de scripts/data_sources.py.
"""

import json
import warnings
import pandas as pd
from pathlib import Path
from data_sources import (
    SOFASCORE_RECORDS, copa_brasil, rating_avg, ajuste_tatico, experiencia_selecao,
)

warnings.filterwarnings("ignore")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

df = pd.DataFrame(SOFASCORE_RECORDS)

factor = 90 / df["minutes"]
df["goals_90"]      = (df["goals"] * factor).round(3)
df["assists_90"]    = (df["assists"] * factor).round(3)
df["g_a_90"]        = ((df["goals"] + df["assists"]) * factor).round(3)
df["shots_90"]      = (df["shots"] * factor).round(2)
df["shots_on_90"]   = (df["shots_on"] * factor).round(2)
df["key_passes_90"] = (df["key_passes"] * factor).round(2)
df["xg_90"]    = (df["xg"] * factor).where(df["xg"].notna()).round(3)
df["xa_90"]    = (df["xa"] * factor).where(df["xa"].notna()).round(3)
df["x_g_a_90"] = ((df["xg"].fillna(0) + df["xa"].fillna(0)) * factor).where(df["xg"].notna()).round(3)

for col in ["copamundial_mp", "copamundial_starts", "copamundial_min", "copamundial_gls", "copamundial_ast"]:
    df[col] = 0

for player_name, stats in copa_brasil.items():
    idx = df[df["player"] == player_name].index[0]
    for k, v in stats.items():
        df.loc[idx, f"copamundial_{k}"] = v

df["rating_avg"]          = df["player"].map(rating_avg)
df["ajuste_tatico"]       = df["player"].map(ajuste_tatico)
df["experiencia_selecao"] = df["player"].map(experiencia_selecao)

cols_order = [
    "player", "team", "league", "season", "matches", "minutes",
    "goals", "assists", "xg", "xa", "shots", "shots_on", "key_passes",
    "yellow_cards", "red_cards", "rating_avg",
    "goals_90", "assists_90", "g_a_90", "xg_90", "xa_90", "x_g_a_90",
    "shots_90", "shots_on_90", "key_passes_90",
    "copamundial_mp", "copamundial_starts", "copamundial_min",
    "copamundial_gls", "copamundial_ast",
    "ajuste_tatico", "experiencia_selecao",
]
df = df[cols_order]

output_path = DATA_DIR / "dataset_substituto_raphinha.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

metadata = {
    "descricao": "Dataset para analise de substituicao de Raphinha na Selecao Brasileira",
    "data_criacao": "2026-06-22",
    "fonte_principal": "SofaScore - coleta manual via extensao Chrome em 22/06/2026",
    "observacoes": [
        "xG e xA indisponiveis para RFPL (sem parceria Opta/StatsBomb).",
        "Ajuste tatico revisado com base nos mapas de calor do SofaScore em 22/06/2026.",
        "Luiz Henrique: heatmap bilateral, nao eh ponta inversa classica.",
        "Rayan: corredor direito, ponta classica.",
        "Endrick: perfil de centroavante, heatmap central.",
        "Raphinha: ponta inversa do terco ofensivo.",
    ],
}
with open(DATA_DIR / "dataset_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"Dataset salvo: {output_path}  shape={df.shape}")

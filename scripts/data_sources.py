"""
Dados brutos do SofaScore — temporada 2025/2026.
Coleta manual via extensao Chrome em 22/06/2026.
"""

raphinha_sofascore = {
    "player": "Raphinha", "team": "FC Barcelona", "league": "La Liga",
    "season": "2025/2026", "matches": 22, "minutes": 1388,
    "goals": 13, "assists": 3, "xg": 10.36, "xa": 5.81,
    "shots": 66, "shots_on": 24, "key_passes": 44,
    "yellow_cards": None, "red_cards": None,
}

luiz_henrique_sofascore = {
    "player": "Luiz Henrique", "team": "Zenit", "league": "Russian Premier League",
    "season": "2025/2026", "matches": 28, "minutes": 2023,
    "goals": 6, "assists": 3, "xg": None, "xa": None,  # RFPL sem Opta/StatsBomb
    "shots": 51, "shots_on": 15, "key_passes": None,
    "yellow_cards": 2, "red_cards": 0,
}

rayan_sofascore = {
    "player": "Rayan", "team": "Bournemouth", "league": "Premier League",
    "season": "2025/2026", "matches": 15, "minutes": 1119,
    "goals": 5, "assists": 2, "xg": 2.91, "xa": 1.82,
    "shots": 29, "shots_on": 8, "key_passes": 14,
    "yellow_cards": None, "red_cards": None,
}

endrick_sofascore = {
    "player": "Endrick", "team": "Olympique Lyonnais", "league": "Ligue 1",
    "season": "2025/2026", "matches": 16, "minutes": 1222,
    "goals": 5, "assists": 7, "xg": 6.56, "xa": 3.23,
    "shots": 50, "shots_on": 26, "key_passes": 30,
    "yellow_cards": None, "red_cards": None,
}

# Copa do Mundo 2026 — FBref (21/06/2026)
copa_brasil = {
    "Raphinha":       {"mp": 2, "starts": 2, "min": 129, "gls": 0, "ast": 0},
    "Luiz Henrique":  {"mp": 1, "starts": 0, "min": 29,  "gls": 0, "ast": 0},
    "Rayan":          {"mp": 1, "starts": 0, "min": 51,  "gls": 0, "ast": 0},
    "Endrick":        {"mp": 1, "starts": 0, "min": 27,  "gls": 0, "ast": 0},
}

rating_avg = {
    "Raphinha": 7.85, "Luiz Henrique": 7.22, "Rayan": 6.56, "Endrick": 7.47,
}

# Scores qualitativos (revisados pos-heatmap 22/06/2026)
ajuste_tatico = {
    "Raphinha": 10, "Luiz Henrique": 7, "Rayan": 7, "Endrick": 4,
}

experiencia_selecao = {
    "Raphinha": 10, "Luiz Henrique": 8, "Endrick": 6, "Rayan": 4,
}

SOFASCORE_RECORDS = [
    raphinha_sofascore, luiz_henrique_sofascore, rayan_sofascore, endrick_sofascore,
]

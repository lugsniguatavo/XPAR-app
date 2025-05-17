import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="XPAR Predictor – Diagnostica", layout="wide")
st.title("XPAR Predictor – I 4 Pareggi Più Probabili di oggi (17/05/2025)")

def calcola_x_power(pct):
    return min(round((pct / 40) * 100, 1), 100)

API_KEY = "2e6f2963b1314ff6ab5e2b92f8a5787f"
headers = { "X-Auth-Token": API_KEY }
competitions = {
    "Serie A": "SA",
    "Serie B": "SB",
    "Ligue 2": "FL2",
    "Segunda Division": "SD"
}

csv_links = {
    "Serie A": "https://www.dropbox.com/scl/fi/cfm3bk521wdp27xqeboa9/I1.csv?rlkey=hipeecyilhnuqzp2kpvfk6slb&dl=1",
    "Serie B": "https://www.dropbox.com/scl/fi/ubszxmlq1fws2bd4ian11/I2.csv?rlkey=y4y8vqd0uacqjdix0chqnpue0&dl=1",
    "Ligue 2": "https://www.dropbox.com/scl/fi/1vw6ym83mnnd2osukid9x/F2.csv?rlkey=z0wgn8s208kn1ktuv13du7ys6&dl=1",
    "Segunda Division": "https://www.dropbox.com/scl/fi/73zanp3vezwos4v7jr5za/SP2.csv?rlkey=10ahw0835njw3bcpxxx6lgyv3&dl=1"
}

# Carico la mappa alias
with open("squadra_alias.json", "r") as f:
    squadra_alias = json.load(f)

def normalizza(nome):
    return squadra_alias.get(nome, nome)

# Carico i CSV
dataframes = {}
for nome, link in csv_links.items():
    try:
        df = pd.read_csv(link)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
        dataframes[nome] = df
    except Exception as e:
        st.error(f"Errore caricando {nome}: {e}")

# Data oggi in formato ISO
oggi_iso = pd.Timestamp.today().strftime("%Y-%m-%d")

match_list = []

# Per ogni campionato, scarico le partite in programma oggi e calcolo X-Power
for nome, code in competitions.items():
    url = f"https://api.football-data.org/v4/competitions/{code}/matches?dateFrom={oggi_iso}&dateTo={oggi_iso}"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        for match in data.get("matches", []):
            casa_api = match["homeTeam"]["name"]
            trasferta_api = match["awayTeam"]["name"]

            casa = normalizza(casa_api)
            trasferta = normalizza(trasferta_api)

            df = dataframes.get(nome)
            if df is None:
                continue

            partite_casa = df[(df["HomeTeam"] == casa) | (df["AwayTeam"] == casa)].sort_values(by="Date", ascending=False).head(15)
            partite_trasferta = df[(df["HomeTeam"] == trasferta) | (df["AwayTeam"] == trasferta)].sort_values(by="Date", ascending=False).head(15)

            x_casa, x_trasferta = None, None
            if len(partite_casa) >= 5:
                pareggi = partite_casa[partite_casa["FTR"] == "D"].shape[0]
                x_casa = calcola_x_power((pareggi / len(partite_casa)) * 100)
            if len(partite_trasferta) >= 5:
                pareggi = partite_trasferta[partite_trasferta["FTR"] == "D"].shape[0]
                x_trasferta = calcola_x_power((pareggi / len(partite_trasferta)) * 100)

            media_score = None
            if x_casa is not None and x_trasferta is not None:
                media_score = round((x_casa + x_trasferta) / 2, 1)

            match_list.append({
                "Campionato": nome,
                "Casa (API)": casa_api,
                "Trasferta (API)": trasferta_api,
                "Casa (CSV)": casa,
                "Trasferta (CSV)": trasferta,
                "X_Power Casa": x_casa,
                "X_Power Trasferta": x_trasferta,
                "X_Match_Score": media_score
            })
    except Exception as e:
        st.error(f"Errore API {nome}: {e}")

df_diagnosi = pd.DataFrame(match_list)

if df_diagnosi.empty:
    st.warning("Oggi non ci sono partite con dati XPAR calcolabili.")
else:
    st.subheader("Diagnosi completa: partite, XPower e media calcolata")
    st.dataframe(df_diagnosi.sort_values(by="X_Match_Score", ascending=False))

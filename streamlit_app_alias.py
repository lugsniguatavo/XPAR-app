import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="XPAR Predictor – Automatizzato", layout="wide")
st.title("XPAR Predictor – I 4 Pareggi Più Probabili di oggi (17/05/2025)")

def calcola_x_power(pct):
    return min(round((pct / 40) * 100, 1), 100)

API_KEY = "2e6f2963b1314ff6ab5e2b92f8a5787f"
headers = { "X-Auth-Token": API_KEY }
competitions = {
    "Serie A": "SA",
    "Serie B": "SB",
    "Ligue 2": "FL2",
    "Segunda División": "SD"
}

csv_links = {
    "Serie A": "https://www.dropbox.com/scl/fi/cfm3bk521wdp27xqeboa9/I1.csv?rlkey=hipeecyilhnuqzp2kpvfk6slb&st=ks5du2uu&dl=1",
    "Serie B": "https://www.dropbox.com/scl/fi/ubszxmlq1fws2bd4ian11/I2.csv?rlkey=y4y8vqd0uacqjdix0chqnpue0&st=ssqs9slg&dl=1",
    "Ligue 2": "https://www.dropbox.com/scl/fi/1vw6ym83mnnd2osukid9x/F2.csv?rlkey=z0wgn8s208kn1ktuv13du7ys6&st=7q7dwd30&dl=1",
    "Segunda División": "https://www.dropbox.com/scl/fi/73zanp3vezwos4v7jr5za/SP2.csv?rlkey=10ahw0835njw3bcpxxx6lgyv3&st=byhjeu7l&dl=1"
}

risultati = []

for nome, link in csv_links.items():
    try:
        df = pd.read_csv(link)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Date', 'HomeTeam', 'AwayTeam', 'FTR'])
        squadre = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel())
        for squadra in squadre:
            partite = df[(df['HomeTeam'] == squadra) | (df['AwayTeam'] == squadra)].sort_values(by='Date', ascending=False).head(10)
            if not partite.empty:
                pareggi = partite[partite['FTR'] == 'D'].shape[0]
                pct = (pareggi / len(partite)) * 100
                score = calcola_x_power(pct)
                risultati.append({
                    'Campionato': nome,
                    'Squadra': squadra,
                    'X_Power_Score': score
                })
    except Exception as e:
        st.error("Errore CSV " + nome + ": " + str(e))

df_score = pd.DataFrame(risultati)

oggi_iso = pd.Timestamp.today().strftime("%Y-%m-%d")
match_list = []

for nome, code in competitions.items():
    url = f"https://api.football-data.org/v4/competitions/{code}/matches?dateFrom={oggi_iso}&dateTo={oggi_iso}"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        for match in data.get("matches", []):
            casa = match['homeTeam']['name']
            trasferta = match['awayTeam']['name']
            x_casa = df_score[df_score['Squadra'] == casa]['X_Power_Score'].max()
            x_trasferta = df_score[df_score['Squadra'] == trasferta]['X_Power_Score'].max()
            if pd.notna(x_casa) and pd.notna(x_trasferta):
                media = round((x_casa + x_trasferta) / 2, 1)
                match_list.append({
                    "Campionato": nome,
                    "Casa": casa,
                    "Trasferta": trasferta,
                    "X_Power_Casa": x_casa,
                    "X_Power_Trasferta": x_trasferta,
                    "X_Match_Score": media
                })
    except Exception as e:
        st.error("Errore API " + nome + ": " + str(e))

df_match = pd.DataFrame(match_list)

if df_match.empty:
    st.warning("Oggi non ci sono partite con dati sufficienti per il calcolo XPAR.")
else:
    top4 = df_match.sort_values(by="X_Match_Score", ascending=False).head(4)
    st.subheader("Le 4 Partite più da pareggio")
    st.dataframe(top4)

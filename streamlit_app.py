
import streamlit as st
import pandas as pd

st.set_page_config(page_title="XPAR Predictor – Pareggi Probabili", layout="wide")
st.title("XPAR Predictor – I 4 Pareggi Più Probabili Oggi")

# Link ai CSV Dropbox
links = {
    "Serie A": "https://www.dropbox.com/scl/fi/cfm3bk521wdp27xqeboa9/I1.csv?rlkey=hipeecyilhnuqzp2kpvfk6slb&st=ks5du2uu&dl=1",
    "Serie B": "https://www.dropbox.com/scl/fi/ubszxmlq1fws2bd4ian11/I2.csv?rlkey=y4y8vqd0uacqjdix0chqnpue0&st=ssqs9slg&dl=1",
    "Ligue 2": "https://www.dropbox.com/scl/fi/1vw6ym83mnnd2osukid9x/F2.csv?rlkey=z0wgn8s208kn1ktuv13du7ys6&st=7q7dwd30&dl=1",
    "Segunda División": "https://www.dropbox.com/scl/fi/73zanp3vezwos4v7jr5za/SP2.csv?rlkey=10ahw0835njw3bcpxxx6lgyv3&st=byhjeu7l&dl=1"
}

def calcola_x_power(pct):
    return min(round((pct / 40) * 100, 1), 100)

risultati = []

for nome, url in links.items():
    try:
        df = pd.read_csv(url)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Date', 'HomeTeam', 'AwayTeam', 'FTR'])
        squadre = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel())
        for squadra in squadre:
            partite = df[(df['HomeTeam'] == squadra) | (df['AwayTeam'] == squadra)]
            partite = partite.sort_values(by='Date', ascending=False).head(10)
            if not partite.empty:
                pareggi = partite[partite['FTR'] == 'D'].shape[0]
                pct = (pareggi / len(partite)) * 100
                score = calcola_x_power(pct)
                risultati.append({
                    'Campionato': nome,
                    'Squadra': squadra,
                    'Pareggi_ultime_10': pareggi,
                    'Percentuale_Pareggi': round(pct, 1),
                    'X_Power_Score': score
                })
    except Exception as e:
        st.error(f"Errore nel file {nome}: {e}")

df_all = pd.DataFrame(risultati)

# Simuliamo incontri tra squadre con punteggio alto
match_simulati = []
for campionato, gruppo in df_all.groupby("Campionato"):
    top_squadre = gruppo.sort_values(by="X_Power_Score", ascending=False).head(8)
    for i in range(0, len(top_squadre) - 1, 2):
        casa = top_squadre.iloc[i]
        trasferta = top_squadre.iloc[i + 1]
        media_score = round((casa["X_Power_Score"] + trasferta["X_Power_Score"]) / 2, 1)
        match_simulati.append({
            "Campionato": campionato,
            "Casa": casa["Squadra"],
            "Trasferta": trasferta["Squadra"],
            "X_Power_Casa": casa["X_Power_Score"],
            "X_Power_Trasferta": trasferta["X_Power_Score"],
            "X_Match_Score": media_score
        })

df_match = pd.DataFrame(match_simulati)
top4 = df_match.sort_values(by="X_Match_Score", ascending=False).head(4)

st.subheader("Le 4 Partite Più da Pareggio")
st.dataframe(top4)

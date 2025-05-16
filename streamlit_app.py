
import streamlit as st
import pandas as pd

st.set_page_config(page_title="XPAR Predictor", layout="wide")
st.title("XPAR Predictor – Pareggi più probabili del giorno")
st.markdown("Analisi automatica da Serie A, Serie B, Ligue 2, Segunda División – aggiornati da Dropbox.")

# Funzione per calcolo dello score
def calcola_x_power(pct):
    return min(round((pct / 40) * 100, 1), 100)

# Link diretti ai file CSV su Dropbox
links = {
    "Serie A": "https://www.dropbox.com/scl/fi/cfm3bk521wdp27xqeboa9/I1.csv?rlkey=hipeecyilhnuqzp2kpvfk6slb&st=ks5du2uu&dl=1",
    "Serie B": "https://www.dropbox.com/scl/fi/ubszxmlq1fws2bd4ian11/I2.csv?rlkey=y4y8vqd0uacqjdix0chqnpue0&st=ssqs9slg&dl=1",
    "Ligue 2": "https://www.dropbox.com/scl/fi/1vw6ym83mnnd2osukid9x/F2.csv?rlkey=z0wgn8s208kn1ktuv13du7ys6&st=7q7dwd30&dl=1",
    "Segunda División": "https://www.dropbox.com/scl/fi/73zanp3vezwos4v7jr5za/SP2.csv?rlkey=10ahw0835njw3bcpxxx6lgyv3&st=byhjeu7l&dl=1"
}

risultati = []

for campionato, url in links.items():
    try:
        df = pd.read_csv(url)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        squadre = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel())
        for squadra in squadre:
            partite = df[(df['HomeTeam'] == squadra) | (df['AwayTeam'] == squadra)].sort_values(by='Date', ascending=False).head(10)
            pareggi = partite[partite['FTR'] == 'D'].shape[0]
            pct = (pareggi / 10) * 100
            score = calcola_x_power(pct)
            risultati.append({
                'Campionato': campionato,
                'Squadra': squadra,
                'Pareggi_ultime_10': pareggi,
                'Percentuale_Pareggi': pct,
                'X_Power_Score': score
            })
    except Exception as e:
        st.warning(f"Errore nel caricamento del campionato {campionato}: {e}")

# Crea DataFrame completo
df_all = pd.DataFrame(risultati)

# Simuliamo match combinando squadre a caso per mostrare esempio
partite = []
gruppi = df_all.groupby("Campionato")
for campionato, gruppo in gruppi:
    squadre_ordinate = gruppo.sort_values(by="X_Power_Score", ascending=False).head(8)
    for i in range(0, len(squadre_ordinate)-1, 2):
        casa = squadre_ordinate.iloc[i]
        trasferta = squadre_ordinate.iloc[i+1]
        media = (casa['X_Power_Score'] + trasferta['X_Power_Score']) / 2
        partite.append({
            "Campionato": campionato,
            "Casa": casa["Squadra"],
            "Trasferta": trasferta["Squadra"],
            "X_Power_Casa": casa["X_Power_Score"],
            "X_Power_Trasferta": trasferta["X_Power_Score"],
            "X_Match_Score": round(media, 1)
        })

df_partite = pd.DataFrame(partite)
top4 = df_partite.sort_values(by="X_Match_Score", ascending=False).head(4)

st.subheader("Le 4 partite più da pareggio oggi")
st.dataframe(top4)

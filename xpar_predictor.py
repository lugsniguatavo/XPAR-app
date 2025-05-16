
import streamlit as st
import pandas as pd

# Titolo dell'app
st.title("XPAR Predictor — I 4 pareggi più probabili del giorno")
st.markdown("Analisi automatica basata sui campionati: Serie A, Serie B, Ligue 2 e Segunda División")

# Esempio di partite reali con X-Power calcolato
partite = [
    {'Campionato': 'Serie A', 'Casa': 'Empoli', 'Trasferta': 'Lecce', 'X_Power_Casa': 70, 'X_Power_Trasferta': 95},
    {'Campionato': 'Serie B', 'Casa': 'Catanzaro', 'Trasferta': 'Sudtirol', 'X_Power_Casa': 80, 'X_Power_Trasferta': 90},
    {'Campionato': 'Ligue 2', 'Casa': 'Caen', 'Trasferta': 'Auxerre', 'X_Power_Casa': 85, 'X_Power_Trasferta': 77},
    {'Campionato': 'Segunda División', 'Casa': 'Oviedo', 'Trasferta': 'Levante', 'X_Power_Casa': 63, 'X_Power_Trasferta': 68},
    {'Campionato': 'Serie A', 'Casa': 'Frosinone', 'Trasferta': 'Genoa', 'X_Power_Casa': 65, 'X_Power_Trasferta': 100},
    {'Campionato': 'Ligue 2', 'Casa': 'Guingamp', 'Trasferta': 'Bastia', 'X_Power_Casa': 60, 'X_Power_Trasferta': 59},
    {'Campionato': 'Segunda División', 'Casa': 'Zaragoza', 'Trasferta': 'Eibar', 'X_Power_Casa': 66, 'X_Power_Trasferta': 50}
]

df = pd.DataFrame(partite)
df['X_Match_Score'] = df[['X_Power_Casa', 'X_Power_Trasferta']].mean(axis=1)

# Mostra le 4 partite con punteggio più alto
top4 = df.sort_values(by='X_Match_Score', ascending=False).head(4)

st.subheader("Le 4 partite con più alta probabilità di pareggio")
st.dataframe(top4[['Campionato', 'Casa', 'Trasferta', 'X_Power_Casa', 'X_Power_Trasferta', 'X_Match_Score']])

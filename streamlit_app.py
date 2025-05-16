
import streamlit as st
import pandas as pd

st.set_page_config(page_title="XPAR Predictor", layout="wide")
st.title("XPAR Predictor – Controllo CSV da Dropbox (Versione Pulita)")

# Link ai CSV Dropbox (con ?dl=1 per download diretto)
links = {
    "Serie A": "https://www.dropbox.com/scl/fi/cfm3bk521wdp27xqeboa9/I1.csv?rlkey=hipeecyilhnuqzp2kpvfk6slb&st=ks5du2uu&dl=1",
    "Serie B": "https://www.dropbox.com/scl/fi/ubszxmlq1fws2bd4ian11/I2.csv?rlkey=y4y8vqd0uacqjdix0chqnpue0&st=ssqs9slg&dl=1",
    "Ligue 2": "https://www.dropbox.com/scl/fi/1vw6ym83mnnd2osukid9x/F2.csv?rlkey=z0wgn8s208kn1ktuv13du7ys6&st=7q7dwd30&dl=1",
    "Segunda División": "https://www.dropbox.com/scl/fi/73zanp3vezwos4v7jr5za/SP2.csv?rlkey=10ahw0835njw3bcpxxx6lgyv3&st=byhjeu7l&dl=1"
}

# Mostra i risultati del test per ogni file
for nome, url in links.items():
    st.markdown(f"### {nome}")
    try:
        df = pd.read_csv(url)
        st.success(f"✅ {nome} caricato correttamente – {len(df)} righe")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Errore caricando {nome}: {e}")

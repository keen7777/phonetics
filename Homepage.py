import streamlit as st
import pandas as pd

data_de = {
    "Artikulationsart/-ort": ["Plosive", "Nasal", "Trill", "Tap or Flap","Fricative","Lateral Frikative","Approximant","Lateral Approximant"],
    "Bilabial": ["p || b", "  || m", "", "","", "", "", ""],
    "Labiodental": ["", "", "", "","f || v", "", "", ""],
    "Dental": ["", "", "", "","", "", "", ""],
    "Alveolar": ["t || d", "  || n", "", "","s | z", "", "", "  || l"],
    "Post_alveolar": ["", "", "", "","ʃ || ʒ", "", "", ""],
    "Retroflex": ["", "", "", "","", "", "", ""],
    "Palatal": ["", "", "", "","ç ||  ", "", "  || j", ""],
    "Velar": ["k || g", "  || ŋ", "", "","x ||  ", "", "", ""],
    "Uvular": ["", "", "", "","  || ʁ", "", "", ""],
    "Pharyngeal": ["", "", "", "","", "", "", ""],
    "Glottal": ["ʔ ||  ", "", "", "","h ||  ", "", "", ""],
}

df_de = pd.DataFrame(data_de)
st.set_page_config(layout="wide")
st.markdown("### IPA Consonant Chart (DE)")



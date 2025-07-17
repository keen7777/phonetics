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


st.title("📚Homepage and Index of Phonetic knowledge and Quizzes")

pages = [
    (0, "Referenz", "all necessary tables and anotomy images"),
    (1, "Quiz_IPA_Chart", "IPA chart, gab fill, symbols only in german"),
    (2, "Quiz_Merkmale_Vokal", "quiz of Vokal Merkmale table"),
    (3, "Quiz_Merkmale_Konsonant", "quiz of Konsonant Merkmale table"),
    (4, "Quiz_Konsonanten_Merkmalmatrix", "gap filling of Konsonant Merkmale table"),
]

st.write("here is index and short introduction of each page")

for num, title, desc in pages:
    st.markdown(f"**{num}. [{title}](./{title})**")
    st.write(f"   - {desc}")
    st.markdown("---")

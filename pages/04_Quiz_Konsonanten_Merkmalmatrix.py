import streamlit as st
import pandas as pd

# ==========================
# Seitenleiste: Symboldefinition
# ==========================
st.sidebar.header("Benutzerdefinierte Symbole")
symbol_correct = st.sidebar.text_input("Symbol für korrekt", value="t")
symbol_wrong = st.sidebar.text_input("Symbol für falsch", value="f")
symbol_empty = st.sidebar.text_input("Standardsymbol für leer", value="--")
symbol_unknown = st.sidebar.text_input("Platzhalter für unvollständig", value="?")
symbol_wrong_mark = st.sidebar.text_input("Präfix zur Fehleranzeige", value="❌")

# ==========================
# Originaldaten (MultiIndex)
# ==========================
stimmehaft = ['p', 't','k','','','','f','s','ʃ','ç','','h','',''] 
stimmelos = ['b', 'd', 'g', 'm', 'n', 'ŋ', 'v', 'z','ʒ','','R','','j','l']
columns_kons = pd.MultiIndex.from_arrays([stimmehaft, stimmelos], names=['[-stimmhaft]', '[+stimmhaft]'])
features_kons = ['[±kons]', '[±son]', '[±kont]', '[±nas]', '[LAB]', '[KOR]', '[±ant]', '[DOR]']
data_kons = pd.DataFrame(symbol_empty, index=features_kons, columns=columns_kons)

# ==========================
# Richtige Merkmale eintragen
# ==========================
for pair in [('p', 'b'), ('t', 'd'), ('k', 'g'), ('', 'm'), ('', 'n'), ('', 'ŋ'),
             ('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'), ('ç', ''), ('', 'R'), ('', 'l')]:
    data_kons.loc['[±kons]', pair] = symbol_correct 
# data_kons.loc['[±kons]',('h', '')] = symbol_wrong
# data_kons.loc['[±kons]',('', 'j')] = symbol_wrong
for pair in [('', 'm'), ('', 'n'), ('', 'ŋ'), ('', 'R'), ('', 'j'), ('', 'l')]:
    data_kons.loc['[±son]', pair] = symbol_correct
for pair in [('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'), ('ç', ''), ('', 'R'), ('h', ''), ('', 'j')]:
    data_kons.loc['[±kont]', pair] = symbol_correct
for pair in [('', 'm'), ('', 'n'), ('', 'ŋ')]:
    data_kons.loc['[±nas]', pair] = symbol_correct
for pair in [('p', 'b'), ('', 'm'), ('f', 'v')]:
    data_kons.loc['[LAB]', pair] = symbol_correct
for pair in [('t', 'd'), ('', 'n'), ('s', 'z'), ('ʃ', 'ʒ'), ('', 'j'), ('', 'l')]:
    data_kons.loc['[KOR]', pair] = symbol_correct
data_kons.loc['[±ant]', ('s', 'z')] = symbol_correct
# data_kons.loc['[±ant]', ('ʃ', 'ʒ')] = symbol_wrong
for pair in [('k', 'g'), ('', 'ŋ'), ('ç', ''), ('', 'R')]:
    data_kons.loc['[DOR]', pair] = symbol_correct

# ==========================
# Umwandlung in einfache Spaltennamen
# ==========================
new_col_names = [f"{a}/{b}" for a, b in data_kons.columns.to_list()]
flat_df = data_kons.copy()
flat_df.columns = new_col_names

# ==========================
# Benutzer-Eingabetabelle
# ==========================
input_df = pd.DataFrame(symbol_unknown, index=flat_df.index, columns=flat_df.columns)

st.title("Konsonanten-Merkmalmatrix (interaktiv)")
st.write("Bitte füllen Sie die folgende Matrix entsprechend den phonologischen Merkmalen aus:")

# ==========================
# Interaktive Eingabe
# ==========================
user_input = st.data_editor(input_df, num_rows="fixed", use_container_width=True)

# ==========================
# Bewertung
# ==========================
if st.button("Antworten einreichen und bewerten"):
    correct = flat_df
    total_cells = correct.size
    correct_count = (user_input == correct).sum().sum()
    score = round(correct_count / total_cells * 100, 2)

    st.success(f"Ihre Punktzahl: {score}% ({correct_count} von {total_cells} richtig)")

    # Fehler markieren
    feedback_df = user_input.copy()
    for row in correct.index:
        for col in correct.columns:
            if user_input.loc[row, col] != correct.loc[row, col]:
                feedback_df.loc[row, col] = f"{symbol_wrong_mark}{user_input.loc[row, col]}"
    
    st.subheader("Ihre Eingaben (falsche Einträge markiert):")
    st.dataframe(feedback_df, use_container_width=True)

    st.subheader("✅Correct answer:")
    st.dataframe(correct, use_container_width=True)


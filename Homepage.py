import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

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
# settings
gb_de = GridOptionsBuilder.from_dataframe(df_de)
gb_de.configure_default_column(sortable=True, filter=True)

# build and display
gridOptions = gb_de.build()
custom_css = {
    ".ag-cell": {
        "border-right": "1px solid #ccc !important",
        "text-align": "center",
        "vertical-align": "middle"
    },
    ".ag-header-cell": {
        "border-right": "1px solid #ccc !important"
    }
}

AgGrid(df_de, gridOptions=gridOptions,fit_columns_on_grid_load=True, custom_css=custom_css)


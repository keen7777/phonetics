import streamlit as st
import pandas as pd

# 原始 IPA 表格数据
data_de = {
    "Artikulationsart/-ort": ["Plosive", "Nasal", "Trill", "Tap or Flap",
                              "Fricative", "Lateral Frikative", "Approximant", "Lateral Approximant"],
    "Bilabial": ["p || b", "m", "", "", "", "", "", ""],
    "Labiodental": ["", "", "", "", "f || v", "", "", ""],
    "Dental": ["", "", "", "", "", "", "", ""],
    "Alveolar": ["t || d", "n", "", "", "s | z", "", "", "l"],
    "Post_alveolar": ["", "", "", "", "ʃ || ʒ", "", "", ""],
    "Retroflex": ["", "", "", "", "", "", "", ""],
    "Palatal": ["", "", "", "", "ç", "", "j", ""],
    "Velar": ["k || g", "ŋ", "", "", "x", "", "", ""],
    "Uvular": ["", "", "", "", "ʁ", "", "", ""],
    "Pharyngeal": ["", "", "", "", "", "", "", ""],
    "Glottal": ["ʔ", "", "", "", "h", "", "", ""],
}

# 转为 DataFrame
df = pd.DataFrame(data_de)
st.title("IPA Chart(DE)")
st.markdown("## Bitte füllen Sie das Formular aus.")

# 创建一个仅包含可填写项的副本用于输入（用户视图）
input_df = df.copy()
answer_df = df.copy()  # 保存标准答案

for row_idx in range(len(df)):
    for col in df.columns[1:]:
        val = df.loc[row_idx, col].strip()
        if val == "":
            input_df.loc[row_idx, col] = ""  # 显示为空
        else:
            # 替换为填写提示
            input_df.loc[row_idx, col] = ""

# 显示可填写表格
st.markdown("Außer diesen IPA-Zeichen kannst du alle anderen Buchstaben ganz normal mit der Tastatur eingeben.")
st.markdown("**ʃ, ʒ, ç, ʔ, ʁ, ŋ**")
st.markdown("Wenn es stimmlose und stimmhafte Laute im Paar gibt, schreib sie bitte so auf, wie unten gezeigt.")
st.markdown("**a/b**, stimmlos/stimmhaft")
edited_df = st.data_editor(input_df, key="ipa_table_edit", num_rows="fixed")

# 提交按钮
if st.button("absenden"):
    st.subheader("Ergibnis")
    score = 0
    total = 0
    for row_idx in range(len(df)):
        art = df.loc[row_idx, "Artikulationsart/-ort"]
        for col in df.columns[1:]:
            correct = answer_df.loc[row_idx, col].strip().replace("||", "/").replace("|", "/").replace(" ", "")
            if correct == "":
                continue
            user = edited_df.loc[row_idx, col].strip().replace(" ", "")
            total += 1
            if user == correct:
                st.success(f"✅ {art} - {col}: richtig ({user})")
                score += 1
            else:
                st.error(f"❌ {art} - {col}: falsch, die richtige Antwort ist {correct}, Aber deine Antwort ist {user}")
    
    st.markdown(f"### Punkt: {score} / {total}")

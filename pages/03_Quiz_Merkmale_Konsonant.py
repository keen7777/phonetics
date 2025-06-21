import streamlit as st
import pandas as pd
import random

# ----------------------------
# 1. 构建音素对和特征矩阵
# ----------------------------

stimmehaft = ['p', 't','k','','','','f','s','ʃ','ç','','h','',''] 
stimmlos = ['b', 'd', 'g', 'm', 'n', 'ŋ', 'v', 'z','ʒ','','R','','j','l']

merged_columns = []
column_pairs = []
for voiceless, voiced in zip(stimmehaft, stimmlos):
    if voiceless and voiced:
        label = f"{voiceless}/{voiced}"
        pair = (voiceless, voiced)
    elif voiceless or voiced:
        label = f"{voiceless} || {voiced}"
        pair = (voiceless, voiced)
    merged_columns.append(label)
    column_pairs.append(pair)

features_kons = ['[±kons]', '[±son]', '[±kont]', '[±nas]', '[LAB]', '[KOR]', '[±ant]', '[DOR]']
data_kons = pd.DataFrame('-', index=features_kons, columns=merged_columns)

def get_col(voiceless, voiced):
    try:
        return merged_columns[column_pairs.index((voiceless, voiced))]
    except ValueError:
        return None

# 填入特征
for voiceless, voiced in [('p', 'b'), ('t', 'd'), ('k', 'g'), ('', 'm'), ('', 'n'), ('', 'ŋ'),
                          ('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'), ('ç', ''), ('', 'R'), ('', 'l')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±kons]', col] = '+'

for voiceless, voiced in [('', 'm'), ('', 'n'), ('', 'ŋ'), ('', 'R'), ('', 'j'), ('', 'l')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±son]', col] = '+'

for voiceless, voiced in [('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'), ('ç', ''), ('', 'R'), ('h', ''), ('', 'j')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±kont]', col] = '+'

for voiceless, voiced in [('', 'm'), ('', 'n'), ('', 'ŋ')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±nas]', col] = '+'

for voiceless, voiced in [('p', 'b'), ('', 'm'), ('f', 'v')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[LAB]', col] = '✓'

for voiceless, voiced in [('t', 'd'), ('', 'n'), ('s', 'z'), ('ʃ', 'ʒ'), ('', 'j'), ('', 'l')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[KOR]', col] = '✓'

for voiceless, voiced in [('s', 'z')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±ant]', col] = '+'

for voiceless, voiced in [('ʃ', 'ʒ')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[±ant]', col] = '-'

for voiceless, voiced in [('k', 'g'), ('', 'ŋ'), ('ç', ''), ('', 'R')]:
    col = get_col(voiceless, voiced)
    if col: data_kons.loc['[DOR]', col] = '✓'

# ----------------------------
# 2. 显示矩阵
# ----------------------------
st.title("Merkmalmatrix des Deutschen nach Hall (2011:132)")
with st.expander("📋 Referenz: ", expanded=False):
    st.dataframe(data_kons, use_container_width=True)


# ----------------------------
# 3. 判断题逻辑 (带文字说明的选项 + 占位符)
# ----------------------------

st.header("🧠 Interaktive Entscheidungsfragen")

# 获取所有题目
all_entries = []
for feature in features_kons:
    for col in merged_columns:
        value = data_kons.loc[feature, col]
        all_entries.append((feature, col, value))

# 初始化会话状态
if "quiz_order" not in st.session_state:
    st.session_state.quiz_order = random.sample(all_entries, len(all_entries))
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# 让用户输入题目数量
num_questions = st.number_input("Wie viele Fragen möchten Sie beantworten?", min_value=1, max_value=len(all_entries), value=5, step=1)

# 当前题目
feature, col, correct_value = st.session_state.quiz_order[st.session_state.quiz_index]

# 添加占位选项并带文字说明
options = ["Bitte auswählen...", '+', '-']
labels = {
    "Bitte auswählen...": "Bitte auswählen...",
    "+": "Richtig (+)",
    "-": "Falsch (-)"
}

user_answer = st.radio(
    f"Phonem [{col}] im Merkmal {feature}: ist die Markierung '+' oder '-'?",
    options=options,
    format_func=lambda x: labels[x],
    index=0,
    key=f"quiz_radio_{st.session_state.quiz_index}"
)

if st.button("Absenden"):
    if user_answer == "Bitte auswählen...":
        st.warning("❗ Bitte wählen Sie eine gültige Antwort aus, bevor Sie fortfahren.")
    else:
        correct_set = ['+', '✓']
        is_correct = (user_answer == '+' and correct_value in correct_set) or (user_answer == '-' and correct_value == '-')

        if is_correct:
            st.success("✅ Richtig!")
            st.session_state.score += 1
            st.session_state.last_result = "correct"
        else:
            st.error(f"❌ Falsch! Richtige Antwort ist `{correct_value}`")
            st.session_state.last_result = "incorrect"

        st.session_state.total += 1

        # 自动跳到下一题
        if st.session_state.quiz_index + 1 < num_questions:
            st.session_state.quiz_index += 1
        else:
            st.success(f"🎉 Test abgeschlossen! Sie haben {st.session_state.score} von {st.session_state.total} richtig beantwortet.")
            

if st.session_state.last_result:
    if st.session_state.last_result == "correct":
        st.info("Super! Weiter zur nächsten Frage.")
    else:
        st.info("Bitte versuchen Sie die nächste Frage.")

if st.button("🔁 Nochmal starten"):
                st.session_state.quiz_order = random.sample(all_entries, len(all_entries))
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.total = 0
                st.session_state.last_result = None
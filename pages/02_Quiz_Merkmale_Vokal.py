import streamlit as st
import pandas as pd
import random

# ----------------------------
# 1. 定义元音和特征矩阵
# ----------------------------

vowels = ['i', 'ɪ', 'y', 'ʏ', 'e', 'ɛ', 'ø', 'œ', 'ɛː', 'aː', 'a', 'o', 'ɔ', 'u', 'ʊ', 'ə']
features = ['[±kons]', '[±hint]', '[±hoch]', '[±tief]', '[±LAB]', '[±gesp]', '[±lang]']

df_vokal = pd.DataFrame(index=features, columns=vowels)
df_vokal.loc['[±kons]'] = '-'  # 所有元音都为 [-kons]

front = ['i', 'ɪ', 'y', 'ʏ', 'e', 'ɛ', 'ø', 'œ', 'ɛː']
back = ['a', 'aː', 'o', 'ɔ', 'u', 'ʊ']
central = ['ə']

for v in front:
    df_vokal.loc['[±hint]', v] = '-'
for v in back:
    df_vokal.loc['[±hint]', v] = '+'
df_vokal.loc['[±hint]', 'ə'] = '+'

high = ['i', 'ɪ', 'y', 'ʏ', 'u', 'ʊ']
low = ['a', 'aː']
mid = set(vowels) - set(high) - set(low) - {'ə'}

for v in high:
    df_vokal.loc['[±hoch]', v] = '+'
for v in low:
    df_vokal.loc['[±hoch]', v] = '-'
df_vokal.loc['[±hoch]', 'ə'] = '-'
for v in mid:
    df_vokal.loc['[±hoch]', v] = '-'

for v in ['a', 'aː']:
    df_vokal.loc['[±tief]', v] = '+'
for v in vowels:
    if v not in ['a', 'aː']:
        df_vokal.loc['[±tief]', v] = '-'

labial = ['y', 'ʏ', 'ø', 'œ', 'o', 'ɔ', 'u', 'ʊ']
for v in labial:
    df_vokal.loc['[±LAB]', v] = '✓'
for v in vowels:
    if v not in labial:
        df_vokal.loc['[±LAB]', v] = '-'

tense = ['i', 'y', 'e', 'ø', 'o', 'u']
lax = ['ɪ', 'ʏ', 'ɛ', 'œ', 'ɛː', 'aː', 'a', 'ɔ', 'ʊ', 'ə']
for v in tense:
    df_vokal.loc['[±gesp]', v] = '+'
for v in lax:
    df_vokal.loc['[±gesp]', v] = '-'

long_vowels = ['ɛː', 'aː', 'i', 'y', 'e', 'ø', 'o', 'u']
short_vowels = ['ɪ', 'ʏ', 'ɛ', 'œ', 'a', 'ɔ', 'ʊ', 'ə']
for v in long_vowels:
    df_vokal.loc['[±lang]', v] = '+'
for v in short_vowels:
    df_vokal.loc['[±lang]', v] = '-'

# 替换缺失值为 '-'，保证一致性
df_vokal.fillna('-', inplace=True)

# ----------------------------
# 2. 显示元音特征矩阵
# ----------------------------

st.title("Merkmalmatrix der deutschen Vokale")
with st.expander("📋 Referenz: Vokale und Merkmale"):
    st.dataframe(df_vokal, use_container_width=True)

# ----------------------------
# 3. 互动判断题 Quiz
# ----------------------------

st.header("🧠 Interaktive Entscheidungsfragen zu Vokalen")

# 构建所有题目列表： (feature, vowel, correct_value)
all_entries = []
for feature in features:
    for vowel in vowels:
        value = df_vokal.loc[feature, vowel]
        all_entries.append((feature, vowel, value))

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

num_questions = st.number_input(
    "Wie viele Fragen möchten Sie beantworten?",
    min_value=1,
    max_value=len(all_entries),
    value=5,
    step=1
)

# 当前题目
feature, vowel, correct_value = st.session_state.quiz_order[st.session_state.quiz_index]

options = ["Bitte auswählen...", '+', '-']  # 这里添加 ✓ 因为表中有 ✓
labels = {
    "Bitte auswählen...": "Bitte auswählen...",
    "+": "Richtig (+)",
    "-": "Falsch (-)"
    # , "✓": "Check (✓)"
}

user_answer = st.radio(
    f"Vokal [{vowel}] im Merkmal {feature}: Was ist die Markierung?",
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
        is_correct = (user_answer in correct_set and correct_value in correct_set) or (user_answer == '-' and correct_value == '-')
        if is_correct:
            st.success("✅ Richtig!")
            st.session_state.score += 1
            st.session_state.last_result = "correct"
        else:
            st.error(f"❌ Falsch! Richtige Antwort ist `{correct_value}`")
            st.session_state.last_result = "incorrect"
        st.session_state.total += 1

        # 跳到下一题或显示结果
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

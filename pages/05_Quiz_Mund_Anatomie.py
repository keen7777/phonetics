import streamlit as st
from PIL import Image

# 题库示例，每题有独立的图片路径和答案
questions = [
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane.",
        "image_path": "anotomy_img/lips.png",
        "answer": "Lippen",
        "explanation": [
            "Die Lippen formen Laute durch Öffnen, Schließen oder Runden.",
            "Bilabial: [p], [b], [m]",
            "Labiodental: [f], [v]",
            "Runden: [y], [ʏ], [ø], [œ], [o], [ɔ], [u], [ʊ]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/teeth.png",
        "answer": "Zähne",
        "explanation": [
            "Die oberen Schneidezähne helfen bei Reiblauten.",
            "Labiodental: [f], [v]",
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/tongue-tip-apex.png",
        "answer": "Zungenspitze",
        "explanation": [
            "Die Zungenspitze berührt oder nähert sich anderen Artikulatoren.",
            "Alveolar: [t], [d], [n], [l], [s], [z]",
            "Post-Alveolar: [ʃ], [ʒ]",
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/tongue-back.png",
        "answer": "Zungenrücken",
        "explanation": [
            "Der Zungenrücken artikuliert mit dem Gaumen oder Velum.",
            "Palatal: [ç], [j]",
            "Velar: [k], [g], [ŋ], [x]"
        ]
    },
    # 可继续添加更多题目...
]

st.title("📝 Lückentext Quiz mit Bildern")
st.markdown("##### ä, ö, ü, ß")
# 选择题目
q_index = st.selectbox("Wähle eine Frage", range(len(questions)), format_func=lambda x: f"Frage {x+1}")

q = questions[q_index]

# 显示题目描述和对应的图片
st.write(q["desc"])
image = Image.open(q["image_path"])
st.image(image, use_container_width=True)

# 填空输入
user_answer = st.text_input("Ihre Antwort:")

# 提交按钮
if st.button("Antwort prüfen"):
    if user_answer.strip().lower() == q["answer"].lower():
        st.success("✅ Richtig!")
    else:
        st.error(f"❌ Falsch! Die richtige Antwort ist: {q['answer']}")

    # 显示解释
    with st.expander("Erklärung"):
        st.write(q["explanation"])

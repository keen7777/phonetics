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
            "Post-Alveolar: [ʃ], [ʒ]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/tongue-back.png",
        "answer": "Zungenrücken",
        "explanation": [
            "Der Zungenrücken ist der hintere Teil der Zunge. Der Zungenrücken liegt unter dem weichen Gaumen.",
            "Palatal: [ç], [j]",
            "Velar: [k], [g], [ŋ], [x]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/alveolar-ridge.png",
        "answer": "Zahndamm",
        "explanation": [
            "Der Zahndamm(Alveolen) ist ein Wulst hinter den oberen Schneidezähnen.",
            "Alveolar: [t], [d], [n], [l], [s], [z]",
            "Post-Alveolar: [ʃ], [ʒ]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/nasal-cavity.png",
        "answer": "Nasenraum",
        "explanation": [
            "Der Nasenraum liegt über dem Gaumen. Der Nasenraum dient als Resonanzraum, wenn das Velum gesenkt ist.",
            "Bilabial; Alveolar; Velum: [m], [n], [ŋ]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/hard-palate.png",
        "answer": "harter Gaumen",
        "explanation": [
            "Der harte Gaumen(Palate) ist der vordere Teil des Gaumens.",
            "Palate: [ç], [j]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/soft-palate.png",
        "answer": "weicher Gaumen",
        "explanation": [
            "Der weiche Gaumen (auch Velum oder Gaumensegel genannt) ist der hintere Teil des Gaumens.",
            "Velum: [k], [g], [ŋ], [x]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/uvula.png",
        "answer": "Zäpfchen",
        "explanation": [
            "Das Halszäpfchen (auch Uvula genannt) ist Teil des weichen Gaumens.(vibrieren)",
            "Uvulum: [ʁ]"
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/pharynx.png",
        "answer": "Rachen",
        "explanation": [
            "Rachen (Pharynx)Der Rachen ist der hintere Teil der Mundhöhle und ein Resonanzraum zwischen Mund, Nase und Kehlkopf. Er spielt eine Rolle beim Stimmklang und beim Schlucken.",
            "Pharynx: null",
            "Der Rachenraum (auch Pharynx genannt) liegt hinter dem Mundraum."
        ]
    },
    {
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane",
        "image_path": "anotomy_img/vocal-folds.png",
        "answer": "Stimmlippen",
        "explanation": [
            "Die Stimmbänder (Stimmlippen) sind schwingungsfähige Strukturen im Kehlkopf. Die Bewegung der Stimmbänder erzeugt die Stimme bei Vokalen und stimmhaften Konsonanten.",
            "stimmhaft/stimmlos"
        ]
    },
    { 
        "desc": "Benennen Sie die im Bild hervorgehobenen Sprechorgane(unter Stimmlippen)",
        "image_path": "anotomy_img/epiglottis.png",
        "answer": "Kehlkopf",
        "explanation": [
            "Kehlkopf (Larynx) Beinhaltet die Stimmlippen; steuert Stimmhaftigkeit.",
            "Der Kehldeckel (auch Epiglottis genannt) befindet sich am Kehlkopfeingang."
        ]
    }
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

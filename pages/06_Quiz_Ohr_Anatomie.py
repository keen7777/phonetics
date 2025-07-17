import streamlit as st
from PIL import Image

# 1. 显示图像
st.title("🔍Lückentext: Beschrift das Bild")

image = Image.open("anotomy_img/ohr_clear.png")  # 替换为你图片的路径
st.image(image, caption="Bitte füllen Sie die Nummern 1 bis 14 aus", use_container_width=True)
st.markdown("##### 1.not case senstive; 2.10, 11, 12 are latin; 3.feel free to use: ä, ö, ü, ß")


# 2. 标准答案（按编号排列）
correct_answers = [
    "Ohrmuschel", "Schallwellen", "äußerer Gehörgang","Trommelfell", "Hammer", "Amboss", "Steigbügel", "ovales Fenster",  # 1-8
    "rundes Fenster", "scala tympani", "scala media", "scala vestibuli", "cortisches Organ", "Basilarmembran"  # 9-14
]

# 3. 表单输入
with st.form("Anotomie_Ohr"):
    user_answers = []
    num_items = 14
    for row_start in range(1, num_items + 1, 5):  # 每行显示7个输入框
        cols = st.columns(5)
        for j in range(5):
            index = row_start + j
            if index > num_items:
                break
            with cols[j]:
                # 将编号作为 label 直接放入 text_input 中
                st.write(f"No. {index}")
                ans = st.text_input(label=f"{index}.", key=f"ans_{index}", label_visibility="visible")
                user_answers.append(ans.strip())

    submitted = st.form_submit_button("✅ Abgeben")


# 4. 判断与反馈
if submitted:
    score = 0
    feedback = []
    for i in range(14):
        user_input = user_answers[i].lower()
        correct = correct_answers[i].lower()
        if user_input == correct:
            feedback.append(f"✅ {i+1}. Richtig: {user_input}")
            score += 1
        else:
            feedback.append(f"❌ {i+1}. Falsch: Ihre Antwort = `{user_input}`, richtig = `{correct}`")

    st.markdown("---")
    st.subheader(f"🎯 Ergebnis: {score}/14 korrekt")
    for f in feedback:
        st.write(f)

    image_a = Image.open("anotomy_img/ohr.png")
    with st.expander("check image with answers: "):
        st.image(image_a, caption="Ohr Anatimie", use_container_width=True)    

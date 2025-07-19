import streamlit as st
import plotly.express as px
import pandas as pd

# 数据输入
data = {
    "Vowel": ['i', 'ɪ', 'y', 'ʏ', 'e', 'ɛ:', 'ɛ', 'ø', 'œ', 'a:', 'a', 'o', 'ɔ', 'u', 'ʊ', 'ə'],
    #"Height": [4, 3.5, 3.9, 3.4, 3, 2, 2, 2.9, 2, 1, 1, 3, 2, 4, 3.5, 2.5],
    "Height": [3, 2.5, 2.9, 2.4, 2, 1, 1, 1.9, 1, 0, 0, 2, 1, 3, 2.5, 1.5],
    "Backness": [4, 3.5, 3.8, 3.3, 3, 2, 1.9, 2.8, 1.7, 1.1, 1, 0, 0, 0, 0.3, 1],
    "Example": ["Miete", "bitte", "über", "schüchtern", "Schnee", "Käse", "Bett",
                "König", "völlig", "Vater", "Apfel", "Ofen", "oft", "Uhr", "Butter", "Suche"]
}

df = pd.DataFrame(data)

# 用户选择高亮元音
selected_vowel = st.selectbox("Choose your Vokal", df["Vowel"])

# 设置颜色和大小用于高亮
df["Color"] = df["Vowel"].apply(lambda v: "crimson" if v == selected_vowel else "lightblue")
df["Size"] = df["Vowel"].apply(lambda v: 28 if v == selected_vowel else 20)

# 使用 Plotly 绘图（x轴反转，y轴正向）
fig = px.scatter(df, 
                 x="Backness", 
                 y="Height", 
                 text="Vowel",
                 color="Color", 
                 size="Size",
                 hover_data=["Vowel", "Example"],
                 )

# 设置坐标轴方向和样式
fig.update_layout(
    title="Vokal Trapezoid",
    xaxis=dict(title="F2 (Vorn → Zentral→ Hinten, Zungenposition)", autorange='reversed'),  # x轴从右到左
    yaxis=dict(title="F1 (geschlossen → Offen(tief), Zungenhöhe)", autorange=False),         # y轴从上到下
    showlegend=False,
    height=600
)
fig.update_traces(textposition='top center', 
                  marker=dict(line=dict(width=2, color='DarkSlateGrey')))

# 显示图表
st.plotly_chart(fig, use_container_width=True)

# 可选的分组方案
group_options = ["default", "hinten?", "hoch?", "tief?", "lang?", "LAB?", "gespannt?"]
selected_group = st.selectbox("distinguish Merkmals?", group_options)

# 分组规则定义
group_labels = {}

if selected_group == "lang?":
    long_vowels = {'i', 'y', 'e', 'ø', 'ɛ:','a:','o', 'u'}
    for v in df["Vowel"]:
        group_labels[v] = "+lang" if v in long_vowels else "-lang"

elif selected_group == "LAB?":
    rounded = {'y', 'ʏ', 'ø', 'œ', 'o', 'ɔ', 'u', 'ʊ'}
    for v in df["Vowel"]:
        group_labels[v] = "+LAB(rund)" if v in rounded else "-LAB"

elif selected_group == "hoch?":
    hoch = {'i', 'ɪ', 'y', 'ʏ', 'u', 'ʊ'}
    for v in df["Vowel"]:
        group_labels[v] = "+hoch" if v in hoch else "-hoch"

elif selected_group == "hinten?":
    hint = {'a:', 'a', 'o', 'u', 'ɔ', 'ʊ', 'ə'}
    for v in df["Vowel"]:
        if v in hint:
            group_labels[v] = "+hint"
        else:
            group_labels[v] = "-hint"

elif selected_group == "gespannt?":
    gesp_vowels = {'i', 'y', 'e', 'ø','o', 'u'}
    for v in df["Vowel"]:
        group_labels[v] = "+gesp" if v in gesp_vowels else "-gesp"

elif selected_group == "tief?":
    tief_vowels = {'a:','a'}
    for v in df["Vowel"]:
        group_labels[v] = "+tief" if v in tief_vowels else "-tief"

else:  # "无分组"
    for v in df["Vowel"]:
        group_labels[v] = "default"

# 添加分组标签列
df["Group"] = df["Vowel"].map(group_labels)

# 设置统一大小，颜色由组别决定
df["Size"] = 24

# 绘图
fig = px.scatter(
    df,
    x="Backness",
    y="Height",
    text="Vowel",
    color="Group",  # 分组上色
    size="Size",
    hover_data=["Vowel", "Example", "Group"],
    color_discrete_sequence=px.colors.qualitative.Set2
)

# 设置坐标轴方向和样式
fig.update_layout(
    title=f"Vokal-Trapez：{selected_group}",
    xaxis=dict(title="F2 (Vorn → Zentral → Hinten)", autorange='reversed'),
    yaxis=dict(title="F1 (Close → Open)", autorange=False),
    height=600,
    showlegend=True
)
fig.update_traces(
    textposition='top center',
    marker=dict(line=dict(width=2, color='DarkSlateGrey'))
)

# 显示图表
st.plotly_chart(fig, use_container_width=True)
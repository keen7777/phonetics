import pandas as pd
import plotly.express as px
from collections import defaultdict
import streamlit as st

# 原始数据
data = {
    "Konsonant": ['p', 'b', 't', 'd', 'k', 'g', 
                  'm', 'n', 'ŋ', 
                  'f', 'v', 's', 'z', 'ʃ', 'ʒ', 'ç', 'ʁ','h',
                  'j','l'],
    "Artikulationsart": [0, 0, 0, 0, 0, 0,   # plosive
                         1, 1, 1,            # nasal
                         2, 2, 2, 2, 2, 2, 2, 2, 2,  # fricative
                         3,                 # approximant
                         4],                # lateral approximant
    "Artikulationsort": [0, 0, 2, 2, 5, 5, 
                         0, 2, 5, 
                         1, 1, 2, 2, 3, 3, 4, 6, 7,
                         4,
                         2],
    "Example": ["Pass", "bitte", "Tiger", "duzen", "Kuss", "gut", 
                "Mutter", "Name", "Ding",
                "fern", "Vase", "wissen", "Sohn", "schon", "Journalist", "ich", "richtig", "Hai",
                "Jahr", "Lust"]
}

# 映射发音方法编号到文字
art_labels = {
    0: "Plosive",
    1: "Nasal",
    2: "Fricative",
    3: "Approximant",
    4: "Lateral Approximant"
}

# 映射发音部位编号到文字
ort_labels = {
    0: "Bilabial",
    1: "Labiodental",
    2: "Alveolar",
    3: "Postalveolar",
    4: "Palatal",
    5: "Velar",
    6: "Uvular",
    7: "Glottal"
}

# 创建 DataFrame 并映射标签
df = pd.DataFrame(data)
df["Artikulationsart_text"] = df["Artikulationsart"].map(art_labels)
df["Artikulationsort_text"] = df["Artikulationsort"].map(ort_labels)

# 处理重叠：稍微偏移每个位置
position_counts = defaultdict(int)
x_offset = []
y_offset = []

for x, y in zip(df["Artikulationsort"], df["Artikulationsart"]):
    key = (x, y)
    count = position_counts[key]
    dx = (count % 2) * 0.15 * (-1)**count
    dy = (count // 2) * 0.15 * (-1)**(count + 1)
    x_offset.append(x + dx)
    y_offset.append(y + dy)
    position_counts[key] += 1

df["x_adj"] = x_offset
df["y_adj"] = y_offset

# 使用 Plotly 绘图
fig = px.scatter(
    df,
    x="x_adj",
    y="y_adj",
    text="Konsonant",
    hover_data=["Example", "Artikulationsart_text", "Artikulationsort_text"],
    color="Artikulationsart_text",
    color_discrete_sequence=px.colors.qualitative.Set2,
    size=[20]*len(df)
)

# 调整标签显示位置
fig.update_traces(textposition='top center')

# 自定义坐标轴
fig.update_layout(
    xaxis=dict(
        title="Artikulationsort",
        tickmode='array',
        tickvals=list(ort_labels.keys()),
        ticktext=list(ort_labels.values())
    ),
    yaxis=dict(
        autorange="reversed",
        title="Artikulationsart",
        tickmode='array',
        tickvals=list(art_labels.keys()),
        ticktext=list(art_labels.values())
    ),
    title="Deutsche Konsonanten nach Artikulationsart und -ort",
    height=500,
    width=1200
)

# 展示图形（使用 streamlit 就用 st.plotly_chart(fig)）
st.plotly_chart(fig, use_container_width=True)
########

# 可选的分组方案
group_options = ["default", "stimmhaft?", "konsonantisch?", "sonarantisch?","kontinuierlisch?","nasal?","LAB?","KOR?","anterior?","DOR?"]
selected_group = st.selectbox("Choose grouping for consonants:", group_options)

group_labels = {}

if selected_group == "stimmhaft?":
    stl = {'p', 't', 'k', 'f', 's','ʃ','ç', 'h'}
    for v in df["Konsonant"]:
        group_labels[v] = "-sth" if v in stl else "+sth"

elif selected_group == "konsonantisch?":
    not_kons = {'h', 'j'}
    for v in df["Konsonant"]:
        group_labels[v] = "-kons" if v in not_kons else "+kons"

elif selected_group == "sonarantisch?":
    son = {'m', 'n','ŋ',
                'ʁ','j','l'}
    for v in df["Konsonant"]:
        group_labels[v] = "+son" if v in son else "-son"  

elif selected_group == "nasal?":
    nas = {'m', 'n','ŋ'}
    for v in df["Konsonant"]:
        group_labels[v] = "+nas" if v in nas else "-nas"    

elif selected_group == "kontinuierlisch?":
    kont = {'f', 'v', 's', 'z', 'ʃ', 'ʒ', 'ç', 'ʁ','h',
                  'j'}
    for v in df["Konsonant"]:
        group_labels[v] = "+kont" if v in kont else "-kont"    

elif selected_group == "LAB?":
    lab = {'f', 'v', 'b', 'p', 'm'}
    for v in df["Konsonant"]:
        group_labels[v] = "+LAB" if v in lab else "-LAB"   

elif selected_group == "KOR?":
    kor = {'t', 'd', 'n', 's', 'z','ʃ', 'ʒ','j','l'}
    for v in df["Konsonant"]:
        group_labels[v] = "+KOR" if v in kor else "-KOR"           

elif selected_group == "DOR?":
    dor = {'k', 'g', 'ŋ', 'ç', 'ʁ'}
    for v in df["Konsonant"]:
        group_labels[v] = "+DOR" if v in dor else "-DOR"    

elif selected_group == "anterior?":
    ant = {'s', 'z'}
    not_ant = {'ʃ', 'ʒ'}
    for v in df["Konsonant"]:
        if v in ant: group_labels[v] = "+ant" 
        elif v in not_ant: group_labels[v] = "-ant"

else:  # default 不分组，所有归为"default"
    for k in df["Konsonant"]:
        group_labels[k] = "default"

######## done

# 将分组标签加到 DataFrame 中
df["Gruppe"] = df["Konsonant"].map(group_labels)

group_list = list(set(group_labels.values()))
custom_color_map = {
    group_list[0]: "green",
    group_list[1] if len(group_list) > 1 else "OTHER": "orange"
}

# 确保所有分组值有对应颜色，超过两个时补灰色
unique_groups = df["Gruppe"].unique()
for g in unique_groups:
    if g not in custom_color_map:
        custom_color_map[g] = "lightgrey"

# 使用 Plotly 绘图（分组着色）
fig = px.scatter(
    df,
    x="x_adj",
    y="y_adj",
    text="Konsonant",
    hover_data=["Example", "Artikulationsart_text", "Artikulationsort_text", "Gruppe"],
    color="Gruppe",
    color_discrete_sequence=px.colors.qualitative.Set2,
    size=[20]*len(df)
)

# 调整标签显示位置
fig.update_traces(textposition='top center')

# 自定义坐标轴
fig.update_layout(
    xaxis=dict(
        title="Artikulationsort",
        tickmode='array',
        tickvals=list(ort_labels.keys()),
        ticktext=list(ort_labels.values())
    ),
    yaxis=dict(
        autorange="reversed",
        title="Artikulationsart",
        tickmode='array',
        tickvals=list(art_labels.keys()),
        ticktext=list(art_labels.values())
    ),
    title=f"Konsonanten-Gruppierung: {selected_group}",
    height=500,
    width=1200
)

# 展示图形
st.plotly_chart(fig, use_container_width=True)

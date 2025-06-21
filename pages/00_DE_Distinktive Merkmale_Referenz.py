import streamlit as st
import pandas as pd

# 第一层表头：音素分类
stimmehaft = ['p', 't','k','','','','f','s','ʃ','ç','','h','',''] 
# 第二层表头：音素本身
stimmelos = ['b', 'd', 'g', 'm', 'n', 'ŋ', 'v', 'z','ʒ','','R','','j','l']

# 创建 MultiIndex 表头
columns_kons = pd.MultiIndex.from_arrays([stimmehaft, stimmelos], names=['[-sth]', '[+sth]'])

# 行标签（音系特征）
features_kons = ['[±kons]', '[±son]', '[±kont]', '[±nas]', '[LAB]', '[KOR]', '[±ant]', '[DOR]']

# 构建一个填充 "-" 的数据框
data_kons = pd.DataFrame('-', index=['[±kons]', '[±son]', '[±kont]', '[±nas]'], columns=columns_kons)

# 填入示例特征
# 设置 [kons] 特征：双唇塞音 p/b、齿龈塞音 t/d、软腭塞音 k/g 为 +, 除去h,j的所有辅音
for pair in [('p', 'b'), ('t', 'd'), ('k', 'g'),
             ('', 'm'), ('', 'n'), ('', 'ŋ'),
             ('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'),
             ('ç', ''),
             ('', 'R'), ('', 'l'),
             ]:
    data_kons.loc['[±kons]', pair] = '+'

# 设置 [son] 特征：m, n, ŋ，R,j,l
for pair in [('', 'm'), ('', 'n'), ('', 'ŋ'),
             ('', 'R'),('', 'j'), ('', 'l'),
             ]:
    data_kons.loc['[±son]', pair] = '+'

# 设置 [kont] 特征：m, n, ŋ，R,j,l
for pair in [('f', 'v'), ('s', 'z'), ('ʃ', 'ʒ'),
             ('ç', ''),
             ('', 'R'), ('h', ''), ('', 'j'), 
             ]:
    data_kons.loc['[±kont]', pair] = '+'    

# 设置 [nas] 特征：m, n, ŋ，R,j,l
for pair in [('','m'), ('','n'), ('','ŋ')]:
    data_kons.loc['[±nas]', pair] = '+'

# 设置 [LAB]：p, b, m, f, v
for pair in [('p', 'b'), 
             ('', 'm'), 
             ('f', 'v')]:
    data_kons.loc['[LAB]', pair] = '✓'

# 设置 [KOR]：t,d; n; s,z; ʃ,ʒ; j; l
for pair in [('t', 'd'), 
             ('', 'n'), 
             ('s', 'z'),('ʃ', 'ʒ'),
             ('', 'j'),
             ('', 'l')]:
    data_kons.loc['[KOR]', pair] = '✓'

# 设置 [ant]：k,g; ŋ; s,z; 
for pair in [('s', 'z')]:
    data_kons.loc['[±ant]', pair] = '+'   

for pair in [('ʃ', 'ʒ')]:
    data_kons.loc['[±ant]', pair] = '-'    

# 设置 [DOR]：k,g; ŋ; s,z; 
for pair in [('k', 'g'), 
             ('', 'ŋ'), 
             ('ç', ''),
             ('', 'R')]:
    data_kons.loc['[DOR]', pair] = '✓'


# 显示标题
st.title("Merkmalmatrix des Deutschen")
st.subheader("Konstanten")

# 显示表格（使用 Streamlit 的 dataframe 支持多级列索引）
st.dataframe(data_kons, use_container_width=True)

#######元音

# 定义元音和特征
vowels = ['i', 'ɪ', 'y', 'ʏ', 'e', 'ɛ', 'ø', 'œ', 'ɛː', 'aː', 'a', 'o', 'ɔ', 'u', 'ʊ', 'ə']
features = ['[±kons]', '[±hint]', '[±hoch]', '[±tief]', '[±LAB]', '[±gesp]', '[±lang]']

# 初始化表格，默认填 "-"
df_vokal = pd.DataFrame('-', index=['[±kons]', '[±hint]', '[±hoch]', '[±tief]', '[±gesp]', '[±lang]'], columns=vowels)
# 初始化时就指定 index 顺序
df_vokal = pd.DataFrame(index=[
    '[±kons]', '[±hint]', '[±hoch]', '[±tief]', '[±LAB]', '[±gesp]', '[±lang]'
], columns=vowels)



# [±kons]：所有元音为 [-kons]
df_vokal.loc['[±kons]'] = '-'

# [±hint]（= [±back]）：
front = ['i', 'ɪ', 'y', 'ʏ', 'e', 'ɛ', 'ø', 'œ', 'ɛː']
back = ['a', 'aː', 'o', 'ɔ', 'u', 'ʊ']
central = ['ə']
for v in front:
    df_vokal.loc['[±hint]', v] = '-'
for v in back:
    df_vokal.loc['[±hint]', v] = '+'
df_vokal.loc['[±hint]', 'ə'] = '+'

# [±hoch]：
high = ['i', 'ɪ', 'y', 'ʏ', 'u', 'ʊ']
for v in high:
    df_vokal.loc['[±hoch]', v] = '+'
low = ['a', 'aː']
for v in low:
    df_vokal.loc['[±hoch]', v] = '-'
df_vokal.loc['[±hoch]', 'ə'] = '-'
mid = set(vowels) - set(high) - set(low) - {'ə'}
for v in mid:
    df_vokal.loc['[±hoch]', v] = '-'

# [±tief]（低元音为 +）：
for v in ['a', 'aː']:
    df_vokal.loc['[±tief]', v] = '+'
for v in vowels:
    if v not in ['a', 'aː']:
        df_vokal.loc['[±tief]', v] = '-'

# [±LAB]：圆唇音为 +，非圆唇为 -
labial = ['y', 'ʏ', 'ø', 'œ', 'o', 'ɔ', 'u', 'ʊ']
for v in labial:
    df_vokal.loc['[±LAB]', v] = '✓'
for v in vowels:
    if v not in labial:
        df_vokal.loc['[±LAB]', v] = ''

# [±gesp]（紧张元音为 +，松弛为 -）
tense = ['i', 'y', 'e', 'ø', 'o', 'u']
lax = ['ɪ', 'ʏ', 'ɛ', 'œ','ɛː', 'aː', 'a', 'ɔ', 'ʊ', 'ə']
for v in tense:
    df_vokal.loc['[±gesp]', v] = '+'
for v in lax:
    df_vokal.loc['[±gesp]', v] = '-'

# [±lang]：长元音为 +，短音为 -
long_vowels = ['ɛː', 'aː', 'i', 'y', 'e', 'ø', 'o', 'u']
short_vowels = ['ɪ', 'ʏ', 'ɛ', 'œ', 'a', 'ɔ', 'ʊ', 'ə']
for v in long_vowels:
    df_vokal.loc['[±lang]', v] = '+'
for v in short_vowels:
    df_vokal.loc['[±lang]', v] = '-'

# 显示结果
# 显示表格（使用 Streamlit 的 dataframe 支持多级列索引）
st.subheader("Vokalen")
st.dataframe(df_vokal, use_container_width=True)


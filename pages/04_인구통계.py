import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding='cp949')
    return df

df = load_data()

st.title("📊 서울시 연령별 인구 분석")

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# -----------------------------
# 선택한 행정구 데이터 추출
# -----------------------------
selected_row = df[df.iloc[:, 0] == selected_district]

# 나이별 데이터 추출
age_columns = df.columns[3:]

ages = []
population = []

for col in age_columns:
    try:
        age = ''.join(filter(str.isdigit, col))

        if age != '':
            ages.append(int(age))
            population.append(int(selected_row[col].values[0]))
    except:
        pass

# -----------------------------
# 그래프 그리기
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    ages,
    population,
    color='hotpink',
    linewidth=3
)

# 제목 및 축 설정
ax.set_title(f"{selected_district} 연령별 인구수", fontsize=18)
ax.set_xlabel("나이", fontsize=13)
ax.set_ylabel("인구수", fontsize=13)

# x축 10살 단위 표시
ax.set_xticks(range(0, 101, 10))

# 구분선
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

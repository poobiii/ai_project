import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# -----------------------------
# 한글 설정
# -----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("population.csv", encoding="cp949")

df = load_data()

st.title("📊 서울시 연령별 인구 분석")

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

# -----------------------------
# 선택 행 데이터
# -----------------------------
selected_row = df[df.iloc[:, 0] == selected_district].iloc[0]

# 연령 컬럼
age_columns = df.columns[3:]

ages = []
population = []

for col in age_columns:

    # 컬럼명에서 숫자 찾기
    match = re.search(r'\d+', str(col))

    if match:

        age = int(match.group())

        try:
            value = pd.to_numeric(selected_row[col])

            # 숫자인 경우만 추가
            if pd.notnull(value):

                ages.append(age)
                population.append(value)

        except:
            continue

# -----------------------------
# 길이 강제 맞춤
# -----------------------------
length = min(len(ages), len(population))

ages = ages[:length]
population = population[:length]

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    ages,
    population,
    color='hotpink',
    linewidth=3,
    linestyle='-',
    marker='o',
    markersize=4
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=20
)

# 축 제목
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# x축 10살 단위
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis='x',
    linestyle='--',
    alpha=0.5
)

# 전체 그리드
ax.grid(True, alpha=0.3)

st.pyplot(fig)

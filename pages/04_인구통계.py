import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

st.title("📊 서울시 연령별 인구 꺾은선 그래프")

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

# -----------------------------
# 선택 데이터
# -----------------------------
selected_row = df[df.iloc[:, 0] == selected_district]

# 연령 컬럼
age_columns = df.columns[3:]

ages = []
population = []

for col in age_columns:

    # 컬럼명에서 숫자 추출
    age = ''.join(filter(str.isdigit, str(col)))

    if age != "":

        try:
            value = selected_row[col].values[0]

            # 숫자로 변환
            ages.append(int(age))
            population.append(float(value))

        except:
            continue

# -----------------------------
# 꺾은선 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    ages,
    population,
    linestyle='-',
    marker='o',
    linewidth=3,
    markersize=5,
    color='hotpink'
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=20
)

# 축 이름
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

# 전체 격자
ax.grid(True, alpha=0.3)

st.pyplot(fig)

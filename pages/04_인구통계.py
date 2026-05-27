import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.read_csv("population.csv", encoding="cp949")
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
# 선택한 행정구 데이터
# -----------------------------
selected_row = df[df.iloc[:, 0] == selected_district]

# 연령 컬럼 추출
age_columns = df.columns[3:]

ages = []
population = []

for col in age_columns:

    # 숫자만 추출
    age_num = ''.join(filter(str.isdigit, str(col)))

    # 숫자가 있는 컬럼만 사용
    if age_num != "":

        try:
            value = selected_row[col].values[0]

            ages.append(int(age_num))
            population.append(int(value))

        except:
            pass

# 길이 맞추기
min_len = min(len(ages), len(population))

ages = ages[:min_len]
population = population[:min_len]

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    ages,
    population,
    color="hotpink",
    linewidth=3
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=18
)

# 축 이름
ax.set_xlabel("나이", fontsize=13)
ax.set_ylabel("인구수", fontsize=13)

# x축 10살 단위
ax.set_xticks(range(0, 101, 10))

# 구분선
ax.grid(
    True,
    linestyle="--",
    alpha=0.5
)

st.pyplot(fig)

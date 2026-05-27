import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# ----------------------------
# 한글 설정
# ----------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ----------------------------
# 데이터 불러오기
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

df = load_data()

st.title("📊 서울시 연령별 인구 꺾은선 그래프")

# ----------------------------
# 행정구 선택
# ----------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# ----------------------------
# 선택한 행 가져오기
# ----------------------------
row = df[df.iloc[:, 0] == selected_district].iloc[0]

# ----------------------------
# 연령 / 인구 데이터 추출
# ----------------------------
ages = []
population = []

for col in df.columns:

    # "0세", "1세", "100세 이상" 같은 컬럼만 찾기
    if "세" in str(col):

        match = re.search(r"\d+", str(col))

        if match:

            age = int(match.group())

            try:
                value = int(str(row[col]).replace(",", ""))

                ages.append(age)
                population.append(value)

            except:
                pass

# ----------------------------
# 데이터프레임으로 정렬
# ----------------------------
graph_df = pd.DataFrame({
    "나이": ages,
    "인구수": population
})

graph_df = graph_df.sort_values("나이")

# ----------------------------
# 그래프
# ----------------------------
fig, ax = plt.subplots(figsize=(15, 7))

ax.plot(
    graph_df["나이"],
    graph_df["인구수"],
    color="hotpink",
    linewidth=3,
    marker="o",
    markersize=4
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=20
)

# 축
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# x축 10살 단위
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

# 전체 격자
ax.grid(True, alpha=0.3)

# 여백 자동조절
plt.tight_layout()

# 출력
st.pyplot(fig)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    layout="wide"
)

# ---------------------------------
# 한글 설정
# ---------------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ---------------------------------
# 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("population.csv", encoding="cp949")

df = load_data()

# ---------------------------------
# 제목
# ---------------------------------
st.title("📊 서울시 연령별 인구 꺾은선 그래프")

# ---------------------------------
# 행정구 선택
# ---------------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

# ---------------------------------
# 선택 행 가져오기
# ---------------------------------
row = df[df.iloc[:, 0] == selected_district].iloc[0]

# ---------------------------------
# 데이터 저장
# ---------------------------------
ages = []
population = []

# ---------------------------------
# 연령별 데이터 추출
# ---------------------------------
for col in df.columns:

    col_str = str(col)

    # "세" 포함 컬럼만 사용
    if (
        "세" in col_str
        and "남" not in col_str
        and "여" not in col_str
    ):

        # 컬럼 안의 모든 숫자 추출
        numbers = re.findall(r"\d+", col_str)

        # 마지막 숫자가 실제 나이
        if numbers:

            age = int(numbers[-1])

            # 100세 이상 처리
            if age > 100:
                age = 100

            try:
                value = pd.to_numeric(
                    str(row[col]).replace(",", ""),
                    errors="coerce"
                )

                if pd.notnull(value):

                    ages.append(age)
                    population.append(int(value))

            except:
                pass

# ---------------------------------
# 데이터프레임 생성
# ---------------------------------
graph_df = pd.DataFrame({
    "나이": ages,
    "인구수": population
})

# 나이순 정렬
graph_df = graph_df.sort_values("나이")

# 중복 제거
graph_df = graph_df.drop_duplicates(subset="나이")

# ---------------------------------
# 그래프 생성
# ---------------------------------
fig, ax = plt.subplots(figsize=(18, 7))

ax.plot(
    graph_df["나이"],
    graph_df["인구수"],
    color="hotpink",
    linewidth=3
)

# ---------------------------------
# 제목
# ---------------------------------
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=22
)

# ---------------------------------
# 축 설정
# ---------------------------------
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# ---------------------------------
# x축
# ---------------------------------
ax.set_xlim(0, 100)

ax.set_xticks(range(0, 101, 10))
ax.set_xticks(range(0, 101, 1), minor=True)

# ---------------------------------
# y축
# ---------------------------------
max_pop = graph_df["인구수"].max()

ax.set_ylim(0, max_pop * 1.1)

ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda x, pos: f"{int(x):,}"
    )
)

# ---------------------------------
# 격자
# ---------------------------------
ax.grid(
    which="major",
    axis="x",
    linestyle="--",
    alpha=0.5
)

ax.grid(
    which="minor",
    axis="x",
    linestyle=":",
    alpha=0.15
)

ax.grid(
    axis="y",
    alpha=0.3
)

# ---------------------------------
# 여백
# ---------------------------------
plt.tight_layout()

# ---------------------------------
# 출력
# ---------------------------------
st.pyplot(fig)

# ---------------------------------
# 데이터표
# ---------------------------------
st.subheader("📋 연령별 인구 데이터")

st.dataframe(
    graph_df,
    use_container_width=True
)

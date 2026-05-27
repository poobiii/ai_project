import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    layout="wide"
)

# ---------------------------------
# 한글 폰트 설정
# ---------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------------
# 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

df = load_data()

# ---------------------------------
# 제목
# ---------------------------------
st.title("📊 서울시 연령별 인구 꺾은선 그래프")

st.write("행정구를 선택하면 연령별 인구수를 확인할 수 있어요!")

# ---------------------------------
# 행정구 선택
# ---------------------------------
districts = df.iloc[:, 0].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

# ---------------------------------
# 선택한 행 가져오기
# ---------------------------------
row = df[df.iloc[:, 0] == selected_district].iloc[0]

# ---------------------------------
# 연령별 데이터 추출
# ---------------------------------
ages = []
population = []

for col in df.columns:

    col_str = str(col)

    # "세" 포함 + 남녀 컬럼 제외
    if (
        "세" in col_str
        and "남" not in col_str
        and "여" not in col_str
    ):

        # 숫자 추출
        match = re.search(r"\d+", col_str)

        if match:

            age = int(match.group())

            try:
                value = int(
                    str(row[col]).replace(",", "")
                )

                ages.append(age)
                population.append(value)

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
fig, ax = plt.subplots(figsize=(15, 7))

ax.plot(
    graph_df["나이"],
    graph_df["인구수"],
    color="hotpink",
    linewidth=3,
    linestyle="-",
    marker="o",
    markersize=4
)

# ---------------------------------
# 제목 및 축
# ---------------------------------
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=22
)

ax.set_xlabel(
    "나이",
    fontsize=14
)

ax.set_ylabel(
    "인구수",
    fontsize=14
)

# ---------------------------------
# x축 설정
# ---------------------------------
ax.set_xlim(0, 100)

ax.set_xticks(range(0, 101, 10))

# ---------------------------------
# 구분선
# ---------------------------------
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

ax.grid(
    True,
    alpha=0.3
)

# ---------------------------------
# 여백 자동 조정
# ---------------------------------
plt.tight_layout()

# ---------------------------------
# 그래프 출력
# ---------------------------------
st.pyplot(fig)

# ---------------------------------
# 데이터 표 출력
# ---------------------------------
st.subheader("📋 연령별 인구 데이터")

st.dataframe(
    graph_df,
    use_container_width=True
)

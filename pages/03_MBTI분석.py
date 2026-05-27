# pages/03_MBTI분석.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="🌍 MBTI 분석기",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 분석기")

st.markdown("""
국가별 MBTI 비율과  
MBTI 유형별 TOP10 국가를 분석해보세요!
""")

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    # pages 폴더 기준 상위 폴더 접근
    df = pd.read_csv("../mbti.csv")

    return df

df = load_data()

# -----------------------------------
# 컬럼 정리
# -----------------------------------
df.columns = df.columns.str.strip()

country_col = df.columns[0]
mbti_cols = list(df.columns[1:])

# 숫자 변환
for col in mbti_cols:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

# -----------------------------------
# 사이드바 메뉴
# -----------------------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "🌎 국가별 MBTI 보기",
        "📊 MBTI별 국가 TOP10"
    ]
)

# ===================================
# 1. 국가별 MBTI 보기
# ===================================
if menu == "🌎 국가별 MBTI 보기":

    st.header("🌎 국가별 MBTI 비율")

    selected_country = st.selectbox(
        "국가를 선택하세요 🇺🇳",
        sorted(df[country_col].unique())
    )

    # 국가 데이터
    row = df[df[country_col] == selected_country].iloc[0]

    mbti_data = {}

    for col in mbti_cols:
        mbti_data[col] = row[col]

    mbti_series = pd.Series(mbti_data)

    # 높은 순 정렬
    mbti_series = mbti_series.sort_values(
        ascending=False
    )

    # -----------------------------------
    # 초록색 그라데이션
    # -----------------------------------
    colors = []

    max_value = mbti_series.max()

    for value in mbti_series:

        ratio = value / max_value

        r = 0.7 - ratio * 0.4
        g = 1.0
        b = 0.7 - ratio * 0.4

        colors.append((r, g, b))

    # -----------------------------------
    # 그래프 생성
    # -----------------------------------
    fig, ax = plt.subplots(figsize=(14, 6))

    bars = ax.bar(
        mbti_series.index,
        mbti_series.values,
        color=colors
    )

    # 값 표시
    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{height:.1f}%",
            ha="center",
            fontsize=9
        )

    ax.set_title(
        f"{selected_country} MBTI Distribution",
        fontsize=20,
        weight="bold"
    )

    ax.set_xlabel("MBTI Type")
    ax.set_ylabel("Percentage (%)")

    plt.xticks(rotation=45)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    st.pyplot(fig)

    # -----------------------------------
    # 순위표
    # -----------------------------------
    st.subheader("🏆 MBTI 순위")

    rank_df = pd.DataFrame({
        "순위": range(1, len(mbti_series)+1),
        "MBTI": mbti_series.index,
        "비율(%)": mbti_series.values
    })

    st.dataframe(
        rank_df,
        use_container_width=True,
        hide_index=True
    )

# ===================================
# 2. MBTI별 국가 TOP10
# ===================================
else:

    st.header("📊 MBTI별 국가 TOP10")

    selected_mbti = st.selectbox(
        "MBTI를 선택하세요 🧠",
        mbti_cols
    )

    # TOP10 추출
    top10 = (
        df[[country_col, selected_mbti]]
        .sort_values(
            by=selected_mbti,
            ascending=False
        )
        .head(10)
    )

    # -----------------------------------
    # 초록색 그라데이션
    # -----------------------------------
    colors = []

    max_value = top10[selected_mbti].max()

    for value in top10[selected_mbti]:

        ratio = value / max_value

        r = 0.7 - ratio * 0.4
        g = 1.0
        b = 0.7 - ratio * 0.4

        colors.append((r, g, b))

    # -----------------------------------
    # 그래프 생성
    # -----------------------------------
    fig, ax = plt.subplots(figsize=(14, 6))

    bars = ax.bar(
        top10[country_col],
        top10[selected_mbti],
        color=colors
    )

    # 값 표시
    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{height:.1f}%",
            ha="center",
            fontsize=9
        )

    ax.set_title(
        f"TOP 10 Countries for {selected_mbti}",
        fontsize=20,
        weight="bold"
    )

    ax.set_xlabel("Country")
    ax.set_ylabel("Percentage (%)")

    plt.xticks(rotation=20)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    st.pyplot(fig)

    # -----------------------------------
    # 순위표
    # -----------------------------------
    st.subheader(f"🏆 {selected_mbti} TOP10 국가")

    result_df = pd.DataFrame({
        "순위": range(1, 11),
        "국가": top10[country_col].values,
        "비율(%)": top10[selected_mbti].values
    })

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

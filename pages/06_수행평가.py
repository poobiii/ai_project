import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================
# 페이지 설정
# =====================
st.set_page_config(
    page_title="서울 미세먼지 분석",
    page_icon="🌫️",
    layout="wide"
)

st.title("🌫️ 서울시 미세먼지 분석 대시보드")
st.markdown("서울시 지역별 미세먼지(PM10) 및 초미세먼지(PM2.5)를 분석합니다.")

# =====================
# 데이터 불러오기
# =====================
@st.cache_data
def load_data():

    project_dir = Path(__file__).resolve().parent.parent
    csv_path = project_dir / "ABCD.csv"

    if not csv_path.exists():
        st.error(f"ABCD.csv 파일을 찾을 수 없습니다.\n\n{csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    df.columns = [
        str(col).replace("﻿", "").strip()
        for col in df.columns
    ]

    df["일시"] = pd.to_datetime(df["일시"])

    return df


df = load_data()

# =====================
# 지역 선택
# =====================
regions = sorted(
    [r for r in df["구분"].unique() if r != "평균"]
)

selected_region = st.selectbox(
    "📍 지역 선택",
    regions
)

# =====================
# 지역 데이터
# =====================
region_df = df[df["구분"] == selected_region].copy()

# =====================
# 지역별 평균 PM10 계산
# =====================
avg_pm10 = (
    df[df["구분"] != "평균"]
    .groupby("구분")["미세먼지(PM10)"]
    .mean()
    .reset_index()
)

avg_pm10 = avg_pm10.sort_values(
    "미세먼지(PM10)",
    ascending=False
).reset_index(drop=True)

avg_pm10["순위"] = avg_pm10.index + 1

# =====================
# 색상
# =====================
colors = []

for i, region in enumerate(avg_pm10["구분"]):

    if region == selected_region:
        colors.append("#ff0000")

    else:
        shade = max(230 - i * 4, 140)
        colors.append(f"rgb({shade},{shade},{shade})")

avg_pm10["색상"] = colors

# =====================
# KPI
# =====================
selected_row = avg_pm10[
    avg_pm10["구분"] == selected_region
]

rank = int(selected_row["순위"].iloc[0])

avg_value = float(
    selected_row["미세먼지(PM10)"].iloc[0]
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🏆 미세먼지 순위",
        f"{rank}위"
    )

with col2:
    st.metric(
        "🌫️ 평균 PM10",
        f"{avg_value:.1f}"
    )

# =====================
# 지역별 순위 그래프
# =====================
st.subheader("📊 지역별 평균 미세먼지 순위")

fig_rank = px.bar(
    avg_pm10,
    x="구분",
    y="미세먼지(PM10)",
    color="색상",
    text="순위",
    color_discrete_map="identity"
)

fig_rank.update_layout(
    height=650,
    showlegend=False,
    xaxis_title="지역",
    yaxis_title="평균 PM10",
)

fig_rank.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# =====================
# 비율 그래프
# =====================
st.subheader(
    f"🥧 {selected_region}의 서울 전체 대비 비율"
)

total_pm10 = avg_pm10["미세먼지(PM10)"].sum()

selected_pm10 = avg_pm10.loc[
    avg_pm10["구분"] == selected_region,
    "미세먼지(PM10)"
].iloc[0]

ratio_df = pd.DataFrame({
    "구분": [
        selected_region,
        "기타 지역"
    ],
    "값": [
        selected_pm10,
        total_pm10 - selected_pm10
    ]
})

fig_pie = px.pie(
    ratio_df,
    names="구분",
    values="값",
    hole=0.55
)

fig_pie.update_traces(
    textinfo="percent+label"
)

fig_pie.update_layout(
    height=500
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# =====================
# 월별 변화
# =====================
st.subheader(
    f"📈 {selected_region} 월별 미세먼지 변화"
)

region_df["월"] = region_df["일시"].dt.month

monthly = (
    region_df
    .groupby("월")[["미세먼지(PM10)", "초미세먼지(PM25)"]]
    .mean()
    .reset_index()
)

fig_month = px.line(
    monthly,
    x="월",
    y=["미세먼지(PM10)", "초미세먼지(PM25)"],
    markers=True
)

fig_month.update_layout(
    height=500,
    xaxis_title="월",
    yaxis_title="농도"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# =====================
# 상관관계
# =====================
st.subheader(
    "🔍 PM10과 PM2.5 관계"
)

scatter_df = region_df.dropna()

fig_scatter = px.scatter(
    scatter_df,
    x="미세먼지(PM10)",
    y="초미세먼지(PM25)",
    opacity=0.6
)

fig_scatter.update_layout(
    height=600
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# =====================
# TOP5 / BOTTOM5
# =====================
col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 미세먼지 높은 지역 TOP5")

    st.dataframe(
        avg_pm10.head(5)[
            ["순위", "구분", "미세먼지(PM10)"]
        ],
        hide_index=True,
        use_container_width=True
    )

with col2:

    st.subheader("🌿 공기 좋은 지역 TOP5")

    st.dataframe(
        avg_pm10.tail(5)
        .sort_values("미세먼지(PM10)")[[
            "구분",
            "미세먼지(PM10)"
        ]],
        hide_index=True,
        use_container_width=True
    )

# =====================
# 원본 데이터
# =====================
with st.expander("📄 원본 데이터 보기"):

    st.dataframe(
        region_df,
        use_container_width=True
    )

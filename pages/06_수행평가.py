import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(
    page_title="서울 미세먼지 분석",
    page_icon="🌫️",
    layout="wide"
)

st.title("🌫️ 서울 미세먼지 분석 대시보드")
st.markdown("서울시 지역별 미세먼지(PM10) 데이터를 분석합니다.")

# -------------------
# 데이터 불러오기
# -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../ABCD.csv")

    # 컬럼명 정리
    df.columns = [
        col.replace("﻿", "").strip()
        for col in df.columns
    ]

    # 날짜 변환
    df["일시"] = pd.to_datetime(df["일시"])

    return df

df = load_data()

# -------------------
# 지역 목록
# -------------------
region_list = sorted(
    [x for x in df["구분"].unique() if x != "평균"]
)

selected_region = st.selectbox(
    "📍 지역 선택",
    region_list
)

# -------------------
# 선택 지역 데이터
# -------------------
region_df = df[df["구분"] == selected_region].copy()

# -------------------
# 평균 미세먼지 계산
# -------------------
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

# -------------------
# 색상 만들기
# 1등 빨강
# 나머지 그라데이션
# -------------------
colors = []

for i in range(len(avg_pm10)):
    if i == 0:
        colors.append("#ff0000")
    else:
        ratio = i / len(avg_pm10)

        r = int(255 - ratio * 120)
        g = int(180 + ratio * 50)
        b = int(180 + ratio * 50)

        colors.append(
            f"rgb({r},{g},{b})"
        )

avg_pm10["색상"] = colors

# -------------------
# 지역 순위 찾기
# -------------------
rank = int(
    avg_pm10[
        avg_pm10["구분"] == selected_region
    ]["순위"].iloc[0]
)

avg_value = float(
    avg_pm10[
        avg_pm10["구분"] == selected_region
    ]["미세먼지(PM10)"].iloc[0]
)

# -------------------
# KPI
# -------------------
c1, c2 = st.columns(2)

with c1:
    st.metric(
        "🏆 지역 순위",
        f"{rank}위"
    )

with c2:
    st.metric(
        "🌫️ 평균 PM10",
        f"{avg_value:.1f}"
    )

# -------------------
# 지역별 미세먼지 비교
# -------------------
st.subheader("📊 지역별 평균 미세먼지 순위")

fig_bar = px.bar(
    avg_pm10,
    x="구분",
    y="미세먼지(PM10)",
    text="미세먼지(PM10)",
    color="색상",
    color_discrete_map="identity"
)

fig_bar.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside"
)

fig_bar.update_layout(
    height=650,
    showlegend=False,
    xaxis_title="지역",
    yaxis_title="평균 PM10",
    plot_bgcolor="white"
)

# 선택 지역 강조
fig_bar.add_vline(
    x=rank-1,
    line_width=3,
    line_dash="dash",
    line_color="blue"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# -------------------
# 월별 변화
# -------------------
st.subheader(f"📈 {selected_region} 월별 미세먼지 변화")

region_df["월"] = region_df["일시"].dt.month

monthly = (
    region_df
    .groupby("월")["미세먼지(PM10)"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    monthly,
    x="월",
    y="미세먼지(PM10)",
    markers=True
)

fig_line.update_layout(
    height=500,
    xaxis_title="월",
    yaxis_title="평균 PM10"
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)

# -------------------
# PM10 / PM2.5 비교
# -------------------
st.subheader("🔍 PM10 vs PM2.5 관계")

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

# -------------------
# 데이터 테이블
# -------------------
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(
        region_df,
        use_container_width=True
    )

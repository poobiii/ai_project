import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")
st.markdown("월과 일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인할 수 있습니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 숫자형 변환
    df["최고기온(℃)"] = pd.to_numeric(df["최고기온(℃)"], errors="coerce")
    df["최저기온(℃)"] = pd.to_numeric(df["최저기온(℃)"], errors="coerce")

    # 월, 일, 연도 추출
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.sidebar.selectbox(
    "일 선택",
    available_days
)

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

filtered = filtered.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

st.subheader(f"📈 {month}월 {day}일의 연도별 기온 변화")

if len(filtered) == 0:
    st.warning("데이터가 없습니다.")
    st.stop()

# -----------------------------
# 무지개색 생성
# -----------------------------
rainbow_colors = px.colors.sequential.Rainbow

line_colors = [
    rainbow_colors[
        int(i * (len(rainbow_colors)-1) / max(len(filtered)-1, 1))
    ]
    for i in range(len(filtered))
]

fig = go.Figure()

# 최고기온 (무지개색)
for i in range(len(filtered)-1):
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"].iloc[i:i+2],
            y=filtered["최고기온(℃)"].iloc[i:i+2],
            mode="lines",
            line=dict(
                color=line_colors[i],
                width=4
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )

# 최고기온 점
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines+markers",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=7),
        name="최고기온 🌈"
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines+markers",
        line=dict(
            color="lightblue",
            width=3
        ),
        marker=dict(size=6),
        name="최저기온 ❄️"
    )
)

fig.update_layout(
    height=650,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    xaxis_title="연도",
    yaxis_title="기온(℃)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# 통계
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "역대 최고기온",
        f"{filtered['최고기온(℃)'].max():.1f}℃"
    )

with col2:
    st.metric(
        "역대 최저기온",
        f"{filtered['최저기온(℃)'].min():.1f}℃"
    )

# 데이터 보기
with st.expander("📋 데이터 보기"):
    st.dataframe(
        filtered[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )

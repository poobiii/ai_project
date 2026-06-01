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

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():

    # cp949 실패 시 utf-8-sig 시도
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8-sig")

    # 컬럼명 정리
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    # 날짜 컬럼 찾기
    date_col = None
    for col in df.columns:
        if "날짜" in col:
            date_col = col
            break

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    # 날짜 변환
    df[date_col] = pd.to_datetime(
        df[date_col].astype(str).str.strip(),
        errors="coerce"
    )

    df = df.dropna(subset=[date_col])

    # 기온 컬럼 찾기
    max_col = None
    min_col = None

    for col in df.columns:
        if "최고기온" in col:
            max_col = col
        if "최저기온" in col:
            min_col = col

    if max_col is None or min_col is None:
        st.error("최고기온 또는 최저기온 컬럼을 찾을 수 없습니다.")
        st.write(df.columns.tolist())
        st.stop()

    # 숫자형 변환
    df[max_col] = pd.to_numeric(df[max_col], errors="coerce")
    df[min_col] = pd.to_numeric(df[min_col], errors="coerce")

    # 연도/월/일 생성
    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df, max_col, min_col

df, max_col, min_col = load_data()

# -------------------------------
# 사이드바
# -------------------------------
st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    range(1, 13)
)

available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

if len(available_days) == 0:
    st.warning("해당 월의 데이터가 없습니다.")
    st.stop()

day = st.sidebar.selectbox(
    "일 선택",
    available_days
)

# -------------------------------
# 데이터 필터링
# -------------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

filtered = filtered.dropna(
    subset=[max_col, min_col]
)

st.subheader(f"📈 {month}월 {day}일의 연도별 기온 변화")

if len(filtered) == 0:
    st.warning("데이터가 없습니다.")
    st.stop()

# -------------------------------
# 그래프
# -------------------------------
fig = go.Figure()

# 최고기온 무지개색
rainbow = px.colors.sequential.Rainbow

for i in range(len(filtered) - 1):

    color_idx = int(
        i * (len(rainbow) - 1)
        / max(len(filtered) - 2, 1)
    )

    fig.add_trace(
        go.Scatter(
            x=filtered["연도"].iloc[i:i+2],
            y=filtered[max_col].iloc[i:i+2],
            mode="lines",
            line=dict(
                color=rainbow[color_idx],
                width=4
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )

# 최고기온 범례
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered[max_col],
        mode="lines+markers",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=8),
        name="🌈 최고기온"
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered[min_col],
        mode="lines+markers",
        line=dict(
            color="lightblue",
            width=3
        ),
        marker=dict(size=6),
        name="❄️ 최저기온"
    )
)

fig.update_layout(
    height=700,
    hovermode="x unified",
    xaxis_title="연도",
    yaxis_title="기온 (℃)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# 통계
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "역대 최고기온",
        f"{filtered[max_col].max():.1f}℃"
    )

with col2:
    st.metric(
        "역대 최저기온",
        f"{filtered[min_col].min():.1f}℃"
    )

# -------------------------------
# 데이터 테이블
# -------------------------------
with st.expander("📋 데이터 보기"):
    st.dataframe(
        filtered[
            ["연도", max_col, min_col]
        ],
        use_container_width=True
    )

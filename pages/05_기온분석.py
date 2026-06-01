import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")
st.markdown("월과 일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인하고 미래 기온을 예측할 수 있습니다.")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8-sig")

    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    date_col = None
    max_col = None
    min_col = None

    for col in df.columns:
        if "날짜" in col:
            date_col = col
        elif "최고기온" in col:
            max_col = col
        elif "최저기온" in col:
            min_col = col

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    if max_col is None or min_col is None:
        st.error("기온 컬럼을 찾을 수 없습니다.")
        st.write(df.columns.tolist())
        st.stop()

    df[date_col] = pd.to_datetime(
        df[date_col].astype(str).str.strip(),
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=[date_col])

    df[max_col] = pd.to_numeric(df[max_col], errors="coerce")
    df[min_col] = pd.to_numeric(df[min_col], errors="coerce")

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
    st.warning("데이터가 없습니다.")
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

if len(filtered) < 5:
    st.warning("예측에 사용할 데이터가 부족합니다.")
    st.stop()

# -------------------------------
# 미래 연도 선택
# -------------------------------
st.sidebar.header("🔮 미래 예측")

future_year = st.sidebar.number_input(
    "예측 연도",
    min_value=int(filtered["연도"].max()) + 1,
    max_value=2500,
    value=2050,
    step=1
)

# -------------------------------
# 선형회귀 예측
# -------------------------------
X = filtered[["연도"]]

max_model = LinearRegression()
max_model.fit(X, filtered[max_col])

pred_max = max_model.predict(
    np.array([[future_year]])
)[0]

min_model = LinearRegression()
min_model.fit(X, filtered[min_col])

pred_min = min_model.predict(
    np.array([[future_year]])
)[0]

# -------------------------------
# 그래프
# -------------------------------
st.subheader(f"📈 {month}월 {day}일 연도별 기온 변화")

fig = go.Figure()

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
        marker=dict(size=7),
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

# 최고기온 예측점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers+text",
        text=["★"],
        textposition="top center",
        marker=dict(
            size=16,
            symbol="star"
        ),
        name=f"{future_year} 최고기온 예측"
    )
)

# 최저기온 예측점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers+text",
        text=["★"],
        textposition="bottom center",
        marker=dict(
            size=16,
            symbol="star"
        ),
        name=f"{future_year} 최저기온 예측"
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
# 예측 결과
# -------------------------------
st.subheader("🔮 미래 기온 예측")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.1f}℃"
    )

st.info(
    "예측값은 선택한 날짜의 과거 데이터를 기반으로 선형회귀 모델이 계산한 값입니다."
)

# -------------------------------
# 데이터 보기
# -------------------------------
with st.expander("📋 사용된 데이터 보기"):
    st.dataframe(
        filtered[
            ["연도", max_col, min_col]
        ],
        use_container_width=True
    )

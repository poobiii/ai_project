# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI Country Analyzer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 분석")
st.write("국가를 선택하면 MBTI 비율을 그래프로 보여줘요!")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types(1).csv")

df = load_data()

# -----------------------------
# 컬럼 정리
# -----------------------------
df.columns = df.columns.str.strip()

# 첫 번째 컬럼 = 국가명
country_col = df.columns[0]

# MBTI 컬럼
mbti_cols = df.columns[1:]

# -----------------------------
# 국가 선택
# -----------------------------
selected_country = st.selectbox(
    "국가 선택 🇺🇳",
    sorted(df[country_col].unique())
)

# -----------------------------
# 선택 국가 데이터
# -----------------------------
row = df[df[country_col] == selected_country].iloc[0]

mbti_data = {}

for col in mbti_cols:
    value = row[col]

    # 퍼센트 문자열 처리
    if isinstance(value, str):
        value = value.replace("%", "").strip()

    mbti_data[col] = float(value)

# Series 변환
mbti_series = pd.Series(mbti_data)

# 정렬
mbti_series = mbti_series.sort_values(ascending=False)

# -----------------------------
# 색상 설정
# 1등 = 노란색
# 나머지 = 하늘색 그라데이션
# -----------------------------
top_type = mbti_series.idxmax()

colors = []

max_value = mbti_series.max()

for idx, value in enumerate(mbti_series):

    if mbti_series.index[idx] == top_type:
        colors.append("#FFD700")  # 노란색
    else:
        ratio = value / max_value

        # 하늘색 → 연한색
        r = 0.6 + (1 - ratio) * 0.3
        g = 0.8 + (1 - ratio) * 0.15
        b = 1.0

        colors.append((r, g, b))

# -----------------------------
# 그래프 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(13, 6))

bars = ax.bar(
    mbti_series.index,
    mbti_series.values,
    color=colors
)

# 값 표시
for bar in bars:
    h = bar.get_height()

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.2,
        f"{h:.1f}%",
        ha="center",
        fontsize=9
    )

# 그래프 꾸미기
ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=20,
    weight="bold"
)

ax.set_xlabel("MBTI Type", fontsize=12)
ax.set_ylabel("Percentage (%)", fontsize=12)

plt.xticks(rotation=45)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)

st.pyplot(fig)

# -----------------------------
# 최고 유형 표시
# -----------------------------
st.success(
    f"🏆 가장 높은 유형은 "
    f"{mbti_series.index[0]} "
    f"({mbti_series.iloc[0]:.1f}%) 입니다!"
)

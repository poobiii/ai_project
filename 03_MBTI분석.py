# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="🌍 Countries MBTI Analyzer",
    page_icon="🌎",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 MBTI 유형 비율을 그래프로 보여줘요!")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 선택
countries = sorted(df["Country"].unique())
selected_country = st.selectbox(
    "국가를 선택하세요 🇺🇳",
    countries
)

# 선택 국가 데이터
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI 데이터만 추출
mbti_columns = df.columns[1:]
mbti_values = country_data[mbti_columns]

# 내림차순 정렬
mbti_values = mbti_values.sort_values(ascending=False)

# 1등 찾기
top_value = mbti_values.iloc[0]

# 색상 만들기
colors = []

for value in mbti_values:
    if value == top_value:
        colors.append("#FFD700")  # 노란색
    else:
        # 하늘색 → 흐려지는 그라데이션
        intensity = value / mbti_values.max()

        r = int(180 + (75 * (1 - intensity)))
        g = int(220 + (25 * (1 - intensity)))
        b = 255

        colors.append((r/255, g/255, b/255))

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    mbti_values.index,
    mbti_values.values,
    color=colors
)

# 값 표시
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.2,
        f"{height:.1f}%",
        ha='center',
        fontsize=9
    )

# 그래프 꾸미기
ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=18,
    fontweight='bold'
)

ax.set_xlabel("MBTI Type", fontsize=12)
ax.set_ylabel("Percentage (%)", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.3)

st.pyplot(fig)

# 최고 유형 출력
st.success(
    f"🏆 {selected_country}에서 가장 높은 유형은 "
    f"'{mbti_values.index[0]}' "
    f"({mbti_values.iloc[0]:.1f}%) 입니다!"
)

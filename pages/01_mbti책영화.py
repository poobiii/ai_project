import streamlit as st

st.set_page_config(
    page_title="MBTI 책 & 영화 추천",
    page_icon="📚",
    layout="centered"
)

# MBTI 추천 데이터
recommendations = {
    "INTJ": {
        "korean_books": [
            ("📘 아몬드", "손원평"),
            ("📗 죽고 싶지만 떡볶이는 먹고 싶어", "백세희")
        ],
        "japanese_books": [
            ("📙 나미야 잡화점의 기적", "히가시노 게이고"),
            ("📕 인간실격", "다자이 오사무")
        ],
        "korean_movies": [
            "🎬 기생충",
            "🎬 독전"
        ],
        "american_movies": [
            "🎥 인터스텔라",
            "🎥 인셉션"
        ]
    },

    "INFP": {
        "korean_books": [
            ("📘 완득이", "김려령"),
            ("📗 아몬드", "손원평")
        ],
        "japanese_books": [
            ("📙 너의 췌장을 먹고 싶어", "스미노 요루"),
            ("📕 밤은 짧아 걸어 아가씨야", "모리미 도미히코")
        ],
        "korean_movies": [
            "🎬 리틀 포레스트",
            "🎬 건축학개론"
        ],
        "american_movies": [
            "🎥 월플라워",
            "🎥 라라랜드"
        ]
    },

    "ENFP": {
        "korean_books": [
            ("📘 불편한 편의점", "김호연"),
            ("📗 달러구트 꿈 백화점", "이미예")
        ],
        "japanese_books": [
            ("📙 너의 이름은", "신카이 마코토"),
            ("📕 세상의 중심에서 사랑을 외치다", "카타야마 쿄이치")
        ],
        "korean_movies": [
            "🎬 극한직업",
            "🎬 스물"
        ],
        "american_movies": [
            "🎥 스파이더맨: 뉴 유니버스",
            "🎥 주토피아"
        ]
    },

    "ISTJ": {
        "korean_books": [
            ("📘 칵테일, 러브, 좀비", "조예은"),
            ("📗 페인트", "이희영")
        ],
        "japanese_books": [
            ("📙 용의자 X의 헌신", "히가시노 게이고"),
            ("📕 1Q84", "무라카미 하루키")
        ],
        "korean_movies": [
            "🎬 변호인",
            "🎬 암살"
        ],
        "american_movies": [
            "🎥 쇼생크 탈출",
            "🎥 포드 V 페라리"
        ]
    }
}

# 나머지 MBTI 자동 추가
all_mbti = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 없는 MBTI는 기본 추천 복사
default_data = recommendations["ENFP"]

for mbti in all_mbti:
    if mbti not in recommendations:
        recommendations[mbti] = default_data


# 제목
st.title("✨ MBTI 책 & 영화 추천기 ✨")
st.write("너의 MBTI에 어울리는 감성 작품들을 추천해줄게 😎💖")

# 선택창
selected_mbti = st.selectbox(
    "👇 MBTI를 골라줘!",
    all_mbti
)

# 버튼
if st.button("📚 추천 보기"):
    data = recommendations[selected_mbti]

    st.success(f"{selected_mbti} 유형에게 어울리는 추천이야 ✨")

    st.markdown("## 🇰🇷 한국 작가 책 추천")
    for title, author in data["korean_books"]:
        st.write(f"{title} - {author}")

    st.markdown("## 🇯🇵 일본 작가 책 추천")
    for title, author in data["japanese_books"]:
        st.write(f"{title} - {author}")

    st.markdown("## 🎬 한국 영화 추천")
    for movie in data["korean_movies"]:
        st.write(movie)

    st.markdown("## 🎥 미국 영화 추천")
    for movie in data["american_movies"]:
        st.write(movie)

    st.balloons()

# 하단 문구
st.markdown("---")
st.caption("💫 오늘 기분 따라 작품 하나 골라보는 건 어때?")

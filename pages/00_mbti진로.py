import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천기",
    page_icon="✨",
    layout="centered"
)

# MBTI별 진로 데이터
career_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 분석가",
            "major": "데이터사이언스과, 컴퓨터공학과",
            "personality": "논리적이고 분석적인 사람에게 잘 어울려!",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "🔬 연구원",
            "major": "생명과학과, 화학과",
            "personality": "혼자 깊게 탐구하는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "창의적이고 아이디어 많은 사람에게 딱!",
            "salary": "평균 연봉 약 5,200만 원"
        },
        {
            "job": "🧪 과학자",
            "major": "물리학과, 화학과",
            "personality": "호기심 많고 탐구하는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 5,300만 원"
        }
    ],

    "ENTJ": [
        {
            "job": "📈 경영 컨설턴트",
            "major": "경영학과, 경제학과",
            "personality": "리더십 있고 추진력 강한 사람 추천!",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "🏢 기업 CEO",
            "major": "경영학과",
            "personality": "목표를 세우고 이끄는 걸 좋아하면 잘 맞아!",
            "salary": "평균 연봉 약 7,000만 원 이상"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케팅 기획자",
            "major": "광고홍보학과, 경영학과",
            "personality": "아이디어 많고 말하는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 4,800만 원"
        },
        {
            "job": "🚀 창업가",
            "major": "경영학과",
            "personality": "도전 좋아하고 새로운 걸 시도하는 타입!",
            "salary": "수익은 다양하지만 성공하면 매우 높아!"
        }
    ],

    "INFJ": [
        {
            "job": "💖 상담사",
            "major": "심리학과, 상담학과",
            "personality": "공감 능력 좋고 사람 고민 들어주는 걸 잘해!",
            "salary": "평균 연봉 약 4,200만 원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과, 국문학과",
            "personality": "감수성 풍부하고 상상력이 뛰어나면 추천!",
            "salary": "수익은 작품에 따라 달라져!"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과, 시각디자인과",
            "personality": "감성적이고 창의적인 사람에게 잘 맞아!",
            "salary": "평균 연봉 약 4,000만 원"
        },
        {
            "job": "🎵 작곡가",
            "major": "실용음악과",
            "personality": "음악 좋아하고 감정 표현 잘하면 추천!",
            "salary": "수익은 활동에 따라 다양해!"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과, 국어교육과",
            "personality": "사람 챙기고 이끄는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🎬 방송 PD",
            "major": "미디어학과, 방송영상학과",
            "personality": "소통 잘하고 책임감 강한 사람 추천!",
            "salary": "평균 연봉 약 5,300만 원"
        }
    ],

    "ENFP": [
        {
            "job": "📸 크리에이터",
            "major": "미디어콘텐츠학과",
            "personality": "끼 많고 밝은 성격이면 완전 잘 맞아!",
            "salary": "수익 차이가 크지만 인기 많으면 높아!"
        },
        {
            "job": "🌍 여행 가이드",
            "major": "관광학과",
            "personality": "활발하고 사람 만나는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "ISTJ": [
        {
            "job": "📑 공무원",
            "major": "행정학과",
            "personality": "꼼꼼하고 책임감 강한 사람 추천!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "💰 회계사",
            "major": "회계학과, 경영학과",
            "personality": "계획적이고 숫자 다루는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 6,000만 원"
        }
    ],

    "ISFJ": [
        {
            "job": "🏥 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람에게 추천!",
            "salary": "평균 연봉 약 4,700만 원"
        },
        {
            "job": "🍀 사회복지사",
            "major": "사회복지학과",
            "personality": "사람 돕는 걸 좋아하면 잘 맞아!",
            "salary": "평균 연봉 약 3,500만 원"
        }
    ],

    "ESTJ": [
        {
            "job": "⚖️ 경찰관",
            "major": "경찰행정학과",
            "personality": "정의감 강하고 리더십 있으면 추천!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🏦 은행원",
            "major": "금융학과, 경제학과",
            "personality": "체계적이고 책임감 강한 사람 추천!",
            "salary": "평균 연봉 약 5,200만 원"
        }
    ],

    "ESFJ": [
        {
            "job": "🩺 치위생사",
            "major": "치위생학과",
            "personality": "친절하고 사람 챙기는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 4,300만 원"
        },
        {
            "job": "🎀 승무원",
            "major": "항공서비스학과",
            "personality": "밝고 서비스 정신 좋은 사람 추천!",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 자동차 정비사",
            "major": "자동차학과",
            "personality": "손으로 직접 만드는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 4,200만 원"
        },
        {
            "job": "🛩️ 파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 집중력 좋은 사람에게 잘 맞아!",
            "salary": "평균 연봉 약 7,000만 원"
        }
    ],

    "ISFP": [
        {
            "job": "💄 메이크업 아티스트",
            "major": "뷰티학과",
            "personality": "감각적이고 섬세한 사람 추천!",
            "salary": "평균 연봉 약 3,800만 원"
        },
        {
            "job": "☕ 바리스타",
            "major": "호텔외식조리과, 카페경영과",
            "personality": "감성적이고 분위기 만드는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 3,300만 원"
        }
    ],

    "ESTP": [
        {
            "job": "🏀 스포츠 트레이너",
            "major": "체육학과",
            "personality": "에너지 넘치고 활동적인 사람 추천!",
            "salary": "평균 연봉 약 4,000만 원"
        },
        {
            "job": "🎬 방송인",
            "major": "방송연예과",
            "personality": "사람들 앞에서 말하는 걸 좋아하면 잘 맞아!",
            "salary": "활동에 따라 다양해!"
        }
    ],

    "ESFP": [
        {
            "job": "🎤 가수",
            "major": "실용음악과",
            "personality": "무대 좋아하고 표현력이 풍부하면 추천!",
            "salary": "활동에 따라 다양해!"
        },
        {
            "job": "🛍️ 패션 디자이너",
            "major": "패션디자인학과",
            "personality": "트렌드에 민감하고 감각 있으면 좋아!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ]
}

st.title("✨ MBTI 진로 추천기 ✨")
st.write("나의 MBTI에 어울리는 진로를 알아보자 😎")

mbti = st.selectbox(
    "👇 MBTI를 선택해줘!",
    list(career_data.keys())
)

if st.button("🔍 진로 추천 보기"):
    st.success(f"{mbti} 유형에게 어울리는 진로야!")

    for career in career_data[mbti]:
        st.markdown("---")
        st.subheader(career["job"])
        st.write(f"📚 **추천 학과:** {career['major']}")
        st.write(f"💡 **잘 맞는 성격:** {career['personality']}")
        st.write(f"💰 **평균 연봉:** {career['salary']}")

    st.balloons()

st.markdown("---")
st.caption("🌟 재미로 보는 추천이니까 너무 진지하게만 생각하지는 말기!")

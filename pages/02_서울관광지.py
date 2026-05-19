import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🇰🇷 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("서울의 인기 관광지를 지도에서 확인해보세요! ✨")

# 관광지 데이터
places = {
    "경복궁": {
        "location": [37.5796, 126.9770],
        "emoji": "🏯",
        "desc": "조선 시대의 대표 궁궐",
        "station": "경복궁역 (3호선)",
        "detail": """
- 한복을 입고 궁궐을 돌아다니며 사진을 찍기 좋아요.
- 근처 서촌에는 감성 카페와 맛집이 많아 산책하기 좋아요.
- 국립고궁박물관과 광화문도 함께 구경할 수 있어요.
"""
    },

    "N서울타워": {
        "location": [37.5512, 126.9882],
        "emoji": "🗼",
        "desc": "서울 야경 명소",
        "station": "명동역 (4호선)",
        "detail": """
- 케이블카를 타고 올라가 서울 야경을 감상할 수 있어요.
- 사랑의 자물쇠 존이 유명해서 관광객들이 많이 방문해요.
- 남산 산책로와 포토존이 많아 데이트 코스로 인기예요.
"""
    },

    "명동": {
        "location": [37.5637, 126.9827],
        "emoji": "🛍️",
        "desc": "쇼핑과 길거리 음식의 중심지",
        "station": "명동역 (4호선)",
        "detail": """
- 다양한 화장품 브랜드와 패션 매장이 모여 있어요.
- 길거리 음식 먹방을 즐기기 좋은 관광 명소예요.
- 밤이 되면 화려한 분위기로 외국인 관광객이 많아요.
"""
    },

    "북촌한옥마을": {
        "location": [37.5826, 126.9830],
        "emoji": "🏡",
        "desc": "전통 한옥이 모여 있는 마을",
        "station": "안국역 (3호선)",
        "detail": """
- 한국 전통 한옥 골목 분위기를 느낄 수 있어요.
- 조용한 골목에서 감성 사진 찍기 좋아요.
- 근처 인사동과 삼청동도 함께 구경하기 좋아요.
"""
    },

    "홍대거리": {
        "location": [37.5563, 126.9220],
        "emoji": "🎵",
        "desc": "젊음과 버스킹 문화의 거리",
        "station": "홍대입구역 (2호선)",
        "detail": """
- 버스킹 공연과 스트릿 문화를 즐길 수 있어요.
- 개성 있는 소품샵과 맛집이 정말 많아요.
- 밤에는 클럽과 다양한 놀거리가 활발해져요.
"""
    },

    "롯데월드타워": {
        "location": [37.5131, 127.1025],
        "emoji": "🌆",
        "desc": "서울 대표 초고층 랜드마크",
        "station": "잠실역 (2호선)",
        "detail": """
- 서울스카이 전망대에서 서울 전경을 볼 수 있어요.
- 롯데월드몰과 아쿠아리움도 함께 즐길 수 있어요.
- 쇼핑, 맛집, 놀이시설이 모두 모여 있는 공간이에요.
"""
    },

    "동대문디자인플라자(DDP)": {
        "location": [37.5665, 127.0092],
        "emoji": "🎨",
        "desc": "독특한 디자인 건축물",
        "station": "동대문역사문화공원역 (2호선)",
        "detail": """
- 미래적인 건축 디자인으로 유명한 장소예요.
- 야간 조명이 예뻐서 밤 산책 코스로 좋아요.
- 전시회와 디자인 굿즈샵을 함께 즐길 수 있어요.
"""
    },

    "한강공원": {
        "location": [37.5207, 126.9396],
        "emoji": "🌊",
        "desc": "서울 시민들의 힐링 장소",
        "station": "여의나루역 (5호선)",
        "detail": """
- 한강 라면과 치킨 피크닉을 즐기기 좋아요.
- 자전거 대여와 유람선 체험도 가능해요.
- 밤에는 야경이 아름다워 산책 명소로 유명해요.
"""
    },

    "인사동": {
        "location": [37.5740, 126.9850],
        "emoji": "🖌️",
        "desc": "전통 문화와 기념품 거리",
        "station": "안국역 (3호선)",
        "detail": """
- 전통 공예품과 기념품 가게가 많아요.
- 한국 전통차 카페를 체험할 수 있어요.
- 골목마다 다양한 먹거리와 전시 공간이 있어요.
"""
    },

    "코엑스": {
        "location": [37.5125, 127.0588],
        "emoji": "📚",
        "desc": "별마당도서관으로 유명한 복합공간",
        "station": "삼성역 (2호선)",
        "detail": """
- 별마당도서관에서 감성 사진을 찍기 좋아요.
- 쇼핑몰과 맛집, 영화관이 함께 있어요.
- K-POP 관련 행사와 전시가 자주 열려요.
"""
    }
}

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 마커 추가
for name, info in places.items():

    folium.Marker(
        location=info["location"],
        popup=f'{info["emoji"]} <b>{name}</b><br>{info["desc"]}',
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 크기 조절 (80%)
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st_folium(m, width=900, height=500)

st.markdown("---")

# 관광지 선택
selected_place = st.selectbox(
    "📍 관광지를 선택해보세요!",
    list(places.keys())
)

# 선택 정보 출력
info = places[selected_place]

st.subheader(f"{info['emoji']} {selected_place}")

st.markdown(f"### 🚇 가까운 지하철역")
st.write(info["station"])

st.markdown("### 🎡 놀거리 & 특징")
st.write(info["detail"])

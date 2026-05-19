import streamlit as st
        "location": [37.5512, 126.9882],
        "emoji": "🗼",
        "desc": "서울 야경 명소"
    },
    {
        "name": "명동",
        "location": [37.5637, 126.9827],
        "emoji": "🛍️",
        "desc": "쇼핑과 길거리 음식의 중심지"
    },
    {
        "name": "북촌한옥마을",
        "location": [37.5826, 126.9830],
        "emoji": "🏡",
        "desc": "전통 한옥이 모여 있는 마을"
    },
    {
        "name": "홍대거리",
        "location": [37.5563, 126.9220],
        "emoji": "🎵",
        "desc": "젊음과 버스킹 문화의 거리"
    },
    {
        "name": "롯데월드타워",
        "location": [37.5131, 127.1025],
        "emoji": "🌆",
        "desc": "서울 대표 초고층 랜드마크"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "location": [37.5665, 127.0092],
        "emoji": "🎨",
        "desc": "독특한 디자인 건축물"
    },
    {
        "name": "한강공원",
        "location": [37.5207, 126.9396],
        "emoji": "🌊",
        "desc": "서울 시민들의 힐링 장소"
    },
    {
        "name": "인사동",
        "location": [37.5740, 126.9850],
        "emoji": "🖌️",
        "desc": "전통 문화와 기념품 거리"
    },
    {
        "name": "코엑스",
        "location": [37.5125, 127.0588],
        "emoji": "📚",
        "desc": "별마당도서관으로 유명한 복합공간"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"{place['emoji']} <b>{place['name']}</b><br>{place['desc']}",
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# 지도 출력
st_folium(m, width=1000, height=600)

st.markdown("---")
st.subheader("📍 관광지 리스트")

for idx, place in enumerate(places, start=1):
    st.markdown(f"**{idx}. {place['emoji']} {place['name']}** - {place['desc']}")

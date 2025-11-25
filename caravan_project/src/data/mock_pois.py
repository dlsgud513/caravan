from typing import List, Dict
from src.models.poi import PointOfInterest

# Mock data for Points of Interest (Campgrounds and Toilets)
# In a real application, this would come from a database or an external API.

MOCK_POIS: Dict[str, List[PointOfInterest]] = {
    "경기도 양평": [
        PointOfInterest(
            name="양평 스타 캠핑장",
            type="campground",
            latitude=37.501,
            longitude=127.51,
            address="경기도 양평군 용문면"
        ),
        PointOfInterest(
            name="용문산 관광단지 공중화장실",
            type="toilet",
            latitude=37.505,
            longitude=127.515,
            address="경기도 양평군 용문면 신점리"
        ),
        PointOfInterest(
            name="두물머리 공중화장실",
            type="toilet",
            latitude=37.529,
            longitude=127.31,
            address="경기도 양평군 양서면"
        ),
    ],
    "강원도 인제": [
        PointOfInterest(
            name="인제 자작나무 숲 캠핑장",
            type="campground",
            latitude=38.05,
            longitude=128.16,
            address="강원도 인제군 인제읍"
        ),
        PointOfInterest(
            name="내린천 휴게소 화장실",
            type="toilet",
            latitude=37.95,
            longitude=128.25,
            address="강원도 인제군 상남면"
        ),
        PointOfInterest(
            name="백담사 공용화장실",
            type="toilet",
            latitude=38.17,
            longitude=128.35,
            address="강원도 인제군 북면 용대리"
        ),
        PointOfInterest(
            name="인제 스피디움 캠핑장",
            type="campground",
            latitude=38.07,
            longitude=128.22,
            address="강원도 인제군 기린면"
        ),
    ],
    "제주도 애월": [
        PointOfInterest(
            name="애월 한담해변 캠핑장",
            type="campground",
            latitude=33.49,
            longitude=126.31,
            address="제주도 제주시 애월읍"
        ),
        PointOfInterest(
            name="곽지해수욕장 공중화장실",
            type="toilet",
            latitude=33.495,
            longitude=126.30,
            address="제주도 제주시 애월읍 곽지리"
        ),
        PointOfInterest(
            name="새별오름 공중화장실",
            type="toilet",
            latitude=33.36,
            longitude=126.36,
            address="제주도 제주시 봉성리"
        ),
    ],
}

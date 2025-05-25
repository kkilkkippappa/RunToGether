from datetime import datetime
from fastapi import APIRouter, HTTPException
import os
import sys
from dotenv import load_dotenv
import utils.km_location as km
import requests

# .env 파일 불러오기
load_dotenv()

# 환경변수 불러오기
weather_api_key = os.getenv("WEATHER_API_KEY")

# 라우터 설정
router = APIRouter(
    prefix="/weather",
)

@router.get("/")
async def start_weather():
    return {"msg": "hello, weather page"}

@router.get("/get_weather")
async def get_weather(latitude: float, longitude: float):
    try:
        # 위경도 → 기상청 격자 변환
        nx, ny = km.latlon_to_grid(latitude, longitude)

        # 현재 날짜 및 시간 계산
        now = datetime.now()
        today = now.strftime("%Y%m%d")
        current_minute = now.minute
        if current_minute < 10:
            today_time = datetime(now.year, now.month, now.day, now.hour-1, 30)
        elif current_minute < 40 and current_minute > 10:
            today_time = datetime(now.year, now.month, now.day, now.hour, 0)
        else:
            today_time = datetime(now.year, now.month, now.day, now.hour, 30)
        time_now = today_time.strftime("%H%M")

        print(f"현재 날짜: {today}, 현재 시간: {time_now}, 격자: ({nx}, {ny})")

        # 기상청 초단기예보 API 호출
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        params = {
            "serviceKey": weather_api_key,
            "pageNo": "1",
            "numOfRows": "1000",
            "dataType": "JSON",
            "base_date": today,
            "base_time": time_now,
            "nx": nx,
            "ny": ny
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # 데이터 파싱
        items = data["response"]["body"]["items"]["item"]
        weather_info = {
            "date": today,
            "temperature": None,
            "humidity": None,
            "weather": None,
            "nx": nx,
            "ny": ny
        }

        for item in items:
            category = item["category"]
            if category == "TMP":
                weather_info["temperature"] = item["fcstValue"]
            elif category == "REH":
                weather_info["humidity"] = item["fcstValue"]
            elif category == "PTY":
                weather_info["weather"] = item["fcstValue"]

        return weather_info

    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"기상청 API 호출 실패: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")

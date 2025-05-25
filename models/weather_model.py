from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import utils.km_location as km

class WeatherModel:
    """
    WeatherModel
    - GPS 또는 IP 기반 위치 정보를 활용하여 기상청 API를 호출하고,
    - 날씨 데이터(TMP, REH, PTY)를 파싱하여,
    - 달리기 적합도(good, soso, bad)를 판단하는 역할을 담당한다.

    역할 및 책임:
    1. 위치 정보(GPS, IP)를 기반으로 nx, ny 계산
    2. nx, ny를 사용해 기상청 API 호출
    3. 날씨 데이터 파싱 및 처리
    4. 날씨 적합도 판단 (good/soso/bad)
    """

    def __init__(self):
        self.weather_url = f"{os.getenv('SERVER_URL')}"
        self.weather_api_key = os.getenv("WEATHER_API_KEY")

        # 날씨 데이터 저장용
        self.weather_info = {
            "date": None,
            "totalCount": None,
            "resultCode": None,
            "resultMsg": None,
            "baseDate": None,
            "baseTime": None,
            "temperature": None,
            "weather": None,
            "humidity": None,
            "nx": None,
            "ny": None
        }

        

    def send_location(self, lat, lon):
        """
        GPS에서 받은 lat, lon → nx, ny로 변환 후 저장.
        이후 날씨 데이터 조회 및 달리기 적합도 판단.
        """
        try:
            nx, ny = km.latlon_to_grid(lat, lon)
            self.weather_info["nx"] = nx
            self.weather_info["ny"] = ny

            self.weather_info = self.get_weather()
            running_status = self.is_good_weather_to_running()

            return {
                'status': 'success',
                'weather_data': self.weather_info,
                'running_status': running_status
            }
        except Exception as e:
            print(f"send_location() 에러: {e}")
            return {'status': 'fail', 'message': str(e)}

    def get_weather(self):
        try:
            nx = self.weather_info.get("nx")
            ny = self.weather_info.get("ny")
            if nx is None or ny is None:
                print("nx, ny 없음: IP 기반 위치로 보충")
                lat, lon = self.get_ip_location()
                if lat is not None and lon is not None:
                    nx, ny = km.latlon_to_grid(lat, lon)
                    self.weather_info["nx"] = nx
                    self.weather_info["ny"] = ny
                else:
                    print("위치 정보 가져오기 실패")
                    return {"resultCode": "ERROR", "resultMsg": "위치 정보 없음"}

            now = datetime.now()
            today = now.strftime("%Y%m%d")
            current_minute = now.minute
            time_now = datetime(now.year, now.month, now.day, now.hour, 0).strftime("%H%M") if current_minute < 30 else datetime(now.year, now.month, now.day, now.hour, 30).strftime("%H%M")

            url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
            params = {
                "serviceKey": self.weather_api_key,
                "pageNo": "1",
                "numOfRows": "1000",
                "dataType": "JSON",
                "base_date": today,
                "base_time": time_now,
                "nx": str(nx),
                "ny": str(ny)
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError as e:
                print(f"JSON 파싱 실패: {e}")
                return {"resultCode": "ERROR", "resultMsg": "JSON 파싱 실패"}

            if not data:
                print("API 응답 데이터 없음")
                return {"resultCode": "ERROR", "resultMsg": "API 응답 없음"}

            self.weather_info = self.parse_jsonData(data)
            return self.weather_info

        except Exception as e:
            print(f"기상청 API 호출 실패: {e}")
            return {"resultCode": "ERROR", "resultMsg": f"API 호출 실패: {e}"}

    
    def get_ip_location(self):
        """
        IP 기반 위치 정보 요청 (https://ipinfo.io)
        반환: (lat, lon) tuple 또는 (None, None)
        """
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            loc = data.get("loc")
            if loc:
                lat_str, lon_str = loc.split(",")
                print(f"ip 기반 경도 : {lat_str} 위도 : {lon_str}")
                return float(lat_str), float(lon_str)
        except Exception as e:
            print(f"IP 위치 정보 가져오기 실패: {e}")
        return None, None

    def parse_jsonData(self, data):
        try:
            header = data["response"]["header"]
            result_msg = header.get("resultMsg", "")

            if result_msg == "NO_DATA":
                return {"resultCode": header.get("resultCode"), "resultMsg": "NO_DATA", "totalCount": 0}

            body = data["response"]["body"]
            items = data["response"]["body"]["items"]["item"]

            parsed = {
                "resultCode": header.get("resultCode"),
                "resultMsg": header.get("resultMsg"),
                "totalCount": body.get("totalCount"),
                "baseDate": items[0].get("baseDate") if items else None,
                "nx": items[0].get("nx") if items else None,
                "ny": items[0].get("ny") if items else None,
                "temperature": None,
                "humidity": None,
                "precipitation": None,  # RN1
                "weather": None,  # PTY 코드
                "sky": None  # SKY 코드
            }

            for i in items:
                category = i.get("category")
                value = i.get("fcstValue")
                if category == "T1H":
                    parsed["temperature"] = float(value) if value is not None else None
                elif category == "REH":
                    parsed["humidity"] = float(value) if value is not None else None
                elif category == "PTY":
                    parsed["weather"] = int(value) if value is not None else 0
                elif category == "RN1":
                    if value in ["-", "강수없음", None, ""]:
                        parsed["precipitation"] = 0.0
                    else:
                        try:
                            parsed["precipitation"] = float(value)
                        except ValueError:
                            parsed["precipitation"] = 0.0
                elif category == "SKY":
                    parsed["sky"] = int(value) if value is not None else None

            return parsed

        except Exception as e:
            print(f"날씨 데이터 파싱 에러: {e}")
            return {}


    def is_good_weather_to_running(self):
        try:
            if self.weather_info.get("resultMsg") == "NO_DATA":
                return "no data"

            temp = self.weather_info.get("temperature")
            humid = self.weather_info.get("humidity")
            pty = self.weather_info.get("weather", 0)  # PTY 코드 (강수형태)

            if temp is None or humid is None:
                print("필수 데이터 없음 (temperature or humidity)")
                return "no data"

            temp = float(temp)
            humid = float(humid)

            if int(pty) != 0:
                return "bad"  # 비, 눈 등 강수 시 무조건 bad

            if 10 <= temp <= 25 and 30 <= humid <= 70:
                return "good"
            elif (temp < 5 or temp > 30) or (humid < 20 or humid > 80):
                return "bad"
            else:
                return "soso"

        except Exception as e:
            print(f"날씨 적합도 판단 실패: {e}")
            return None
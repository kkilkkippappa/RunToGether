from dotenv import load_dotenv
import os,sys, requests
# 테스트용 API 호출
api_key = os.getenv("WEATHER_API_KEY")

def parse_ultra_srt_fcst(data: dict) -> dict:
    # 1. 전체 구조 접근
    header = data["response"]["header"]
    result_msg = header.get("resultMsg", "")
    if "no_data" in result_msg.lower():
        return {
                    "resultCode": header.get("resultCode"),
                    "resultMsg": "no data",
                    "totalCount": 0,
                    "baseDate": None,
                    "nx": None,
                    "ny": None,
                    "forecasts": []
                }

    body   = data["response"]["body"]
    items  = body["items"]["item"]
    
    # 2. 기본 정보 세팅
    parsed = {
        "resultCode": header.get("resultCode"),
        "resultMsg":  header.get("resultMsg"),
        "totalCount": body.get("totalCount"),
        # baseDate/baseTime/nx/ny는 모든 아이템이 동일하므로 첫 번째에서 추출
        "baseDate":  items[0].get("baseDate") if items else None,
        "baseTime":  items[0].get("baseTime") if items else None,
        "nx":         items[0].get("nx")       if items else None,
        "ny":         items[0].get("ny")       if items else None,
        "forecasts": []  # 시간별 예보를 담을 곳
    }
    
    # 3. 시간별로 묶기
    forecasts_by_time: dict[str, dict] = {}
    for it in items:
        t = it["fcstTime"]
        if t not in forecasts_by_time:
            forecasts_by_time[t] = {
                "fcstDate": it["fcstDate"],
                "fcstTime": t
            }
        # category에 따라 키를 동적으로 추가
        forecasts_by_time[t][ it["category"] ] = it["fcstValue"]
    
    # 4. 리스트 형태로 변환
    parsed["forecasts"] = list(forecasts_by_time.values())
    return parsed

test_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
test_params = {
    "serviceKey": api_key,
    "pageNo": "1",
    "numOfRows": "10",  # 테스트를 위해 적은 수의 데이터 요청
    "dataType": "JSON",
    "base_date": "20250520",
    "base_time": "1600",
    "nx": "60",  # 테스트용 좌표
    "ny": "121"
}

test_response = requests.get(test_url, params=test_params)
test_json = test_response.json()
print(f"테스트 응답: {test_response.text[:500]}")


test2 = parse_ultra_srt_fcst(test_json)
print("end")
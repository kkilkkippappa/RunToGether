from plyer import gps
import requests
from dotenv import load_dotenv
import os

class GPSModel:
    def __init__(self):
        self.gps = gps
        self.current_location = None
        self.is_running = False
        self.location_callback = None

    def start_gps(self):
        try:
            # 모바일 환경이면서 GPS 구현된다면
            self.gps.configure(on_location=self._on_location)
            self.gps.start()
            self.is_running = True
            return True
        except NotImplementedError:
            print("GPS가 지원되지 않는 플랫폼입니다.")
            #return False
            
            #PC 테스팅 환경
            print("GPS 미지원. PC 테스팅 용 가짜 좌표 반환합니다.")
            location = self.get_ip_location()
            if location:
                self._on_location(**location)
            self.is_running = True
            return True
    
    def stop_gps(self):
        if self.is_running:
            try:
                self.gps.stop()
            except NotImplementedError:
                print("GPS가 지원되지 않는 플랫폼입니다. PC 테스팅 환경에서는 무시됩니다.")
            finally:
                self.is_running = False
    
    def refresh_gps(self):
        """GPS 위치 정보를 갱신합니다."""
        if not self.is_running:
            # GPS가 꺼져 있으면 시작
            return self.start_gps()
        else:
            # 이미 실행 중이면 현재 위치 반환
            if self.current_location and self.location_callback:
                self.location_callback(self.current_location)
            return True
    
    def _on_location(self, **kwargs):
        # GPS 하드웨어로부터 위치 정보를 받는 내부 콜백
        self.current_location = kwargs
        # 등록된 콜백이 있으면 호출
        if self.location_callback:
            self.location_callback(kwargs)
    
    def get_current_location(self):
        return self.current_location
    
    def set_callback(self, callback):
        # Presenter에서 처리할 콜백 등록
        self.location_callback = callback 

    def get_ip_location(self):
        # 함수 콜링 시에 외부ip 기반 서비스 위도,경도 가져오기
        try:
            resp = requests.get("http://ip-api.com/json/")
            data = resp.json()
            return {
                'lat' : data.get('lat'),
                'lon' : data.get('lon')
            }
            print(f"ip lat : {data.get('lat')}  lon : {data.get('lon')}")
        except Exception as e:
            print(f"IP 위치 조회 실패 : {e}")
            return None
        
    def send_location_to_server(self):
        pass

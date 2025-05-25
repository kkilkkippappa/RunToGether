class GPSController:
    def __init__(self, model, view, weather_model):
        self.model = model
        self.view = view
        self.weather_model = weather_model

        # View의 버튼 콜백 연결
        self.view.set_gps_button_callback(self.toggle_gps)

        # Model의 위치 데이터 콜백 연결
        self.model.set_callback(self.on_location_updated)

    def toggle_gps(self):
        if not self.model.is_running:
            success = self.model.start_gps()
            if success:
                self.view.set_gps_button_state(True)
                self.model.refresh_gps()  # 첫 위치 갱신 시도
        else:
            self.model.stop_gps()
            self.view.set_gps_button_state(False)

    def on_location_updated(self, location_data):
        # GPS 데이터 View에 표시
        self.view.update_gps_display(location_data)

        # 위치 정보 유효 시 → 날씨 데이터 요청
        if location_data and 'lat' in location_data and 'lon' in location_data:
            self.send_location(location_data['lat'], location_data['lon'])

        # 위치 수신 후 GPS 자동 종료 + 버튼 상태 복원
        self.model.stop_gps()
        self.view.set_gps_button_state(False)

    def send_location(self, lat, lon):
        result = self.weather_model.send_location(lat, lon)
        if result and result.get("status") == "success":
            self.view.update_weather_display(result["weather_data"], result["running_status"])
        else:
            self.view.update_weather_display(None, None)

    def update_weather_data(self):
        data = self.weather_model.get_weather()
        weather_status = self.weather_model.is_good_weather_to_running()
        self.view.update_weather_display(data, weather_status)

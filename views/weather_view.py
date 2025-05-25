from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from views.base_view import BaseView
from utils.font_manager import get_font_name

class WeatherView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = None
        self.gps_btn_callback = None

    def setup_ui(self):
        self.theme_primary_color = (0.1, 0.47, 0.82, 1)  # #1976D2 블루
        self.theme_good_color = (0.0, 0.7, 0.0, 1)       # 그린
        self.theme_warn_color = (0.9, 0.0, 0.0, 1)       # 레드

        self.main_layout = MDFloatLayout()

        # 상단: 위치 정보
        self.location_label = MDLabel(
            text="위치 정보 없음",
            font_name=get_font_name(),
            halign='center',
            theme_text_color="Custom",
            text_color=self.theme_primary_color,
            font_style="H6",
            size_hint=(1, None),
            pos_hint={"top": 0.95},
            height=dp(40)
        )
        self.main_layout.add_widget(self.location_label)

        # 중간: 날씨 정보 카드
        self.weather_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            radius=[dp(12)],
            md_bg_color=(0.95, 0.95, 0.95, 1),
            size_hint=(0.9, None),
            height=dp(200),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )

        self.temp_label = MDLabel(text="🌡️ 온도: -", halign="left", font_style="Body1", font_name=get_font_name())
        self.humid_label = MDLabel(text="💧 습도: -", halign="left", font_style="Body1", font_name=get_font_name())
        self.rain_label = MDLabel(text="☔ 강수: -", halign="left", font_style="Body1", font_name=get_font_name())
        self.sky_label = MDLabel(text="☁️ 하늘상태: -", halign="left", font_style="Body1", font_name=get_font_name())

        self.weather_card.add_widget(self.temp_label)
        self.weather_card.add_widget(self.humid_label)
        self.weather_card.add_widget(self.rain_label)
        self.weather_card.add_widget(self.sky_label)
        self.main_layout.add_widget(self.weather_card)

        # 하단: 러닝 적합도 카드
        self.status_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            radius=[dp(12)],
            md_bg_color=(0.95, 0.95, 0.95, 1),
            size_hint=(0.9, None),
            height=dp(80),
            pos_hint={"center_x": 0.5, "y": 0.15}
        )

        self.status_label = MDLabel(
            text="러닝 적합도: 알 수 없음",
            font_style="H5",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_name=get_font_name()
        )
        self.status_card.add_widget(self.status_label)
        self.main_layout.add_widget(self.status_card)

        # 하단 플로팅 GPS 버튼
        self.gps_button = MDFloatingActionButton(
            icon="crosshairs-gps",
            text="GPS 시작",
            md_bg_color=self.theme_primary_color,
            pos_hint={"center_x": 0.95, "y": 0.05},
            size_hint=(None, None),
            size=(dp(56), dp(56))
        )
        self.gps_button.bind(on_press=self._on_gps_button_press)
        self.main_layout.add_widget(self.gps_button)

        self.add_widget(self.main_layout)

    def _on_gps_button_press(self, instance):
        if self.gps_btn_callback:
            self.gps_btn_callback()

    def set_gps_button_callback(self, callback):
        self.gps_btn_callback = callback

    def set_gps_button_state(self, is_active):
        self.gps_button.icon = "stop" if is_active else "crosshairs-gps"
        self.gps_button.md_bg_color = (1, 0, 0, 1) if is_active else self.theme_primary_color

    def update_gps_display(self, gps_data):
        if gps_data and 'lat' in gps_data and 'lon' in gps_data:
            lat = gps_data.get('lat', 0)
            lon = gps_data.get('lon', 0)
            self.location_label.text = f'위도: {lat:.6f} / 경도: {lon:.6f}'
        else:
            self.location_label.text = 'GPS 정보를 불러오는데 실패했습니다.'

    def update_weather_display(self, weather_data, weather_status):
        if weather_data:
            if weather_data != 'no data':
    
                self.temp_label.text = f"온도: {weather_data.get('temperature', 'N/A')}°C"
                self.humid_label.text = f"습도: {weather_data.get('humidity', 'N/A')}%"
                self.rain_label.text = f"강수: {weather_data.get('precipitation', 'N/A')}mm"
                sky_code = weather_data.get('sky', 'N/A')
                sky_text = {1: "맑음", 3: "구름많음", 4: "흐림"}.get(int(sky_code), "알 수 없음") if sky_code != 'N/A' else "알 수 없음"
                self.sky_label.text = f"하늘상태: {sky_text}"
            else:
                # no data일 경우 임의의 데이터 넣자
                self.temp_label.text = f"온도: {weather_data.get('temperature', 'no data')}°C"
                self.humid_label.text = f"습도: {weather_data.get('humidity', 'no data')}%"
                self.rain_label.text = f"강수: {weather_data.get('precipitation', 'no data')}mm"
                sky_code = weather_data.get('sky', 'N/A')
                sky_text = {1: "맑음", 3: "구름많음", 4: "흐림"}.get(int(sky_code), "no data") if sky_code != 'N/A' else "알 수 없음"
                self.sky_label.text = f"하늘상태: {sky_text}"

            status_messages = {
                "good": ("달리기 좋은 날씨입니다.", self.theme_good_color),
                "soso": ("달리기 적당한 날씨입니다.", (0.7, 0.7, 0, 1)),
                "bad": ("달리기 좋지 않은 날씨입니다.", self.theme_warn_color)
            }

            text, color = status_messages.get(weather_status, ("러닝 적합도: 알 수 없음", (0, 0, 0, 1)))
            self.status_label.text = text
            self.status_label.text_color = color
        else:
            self.temp_label.text = "온도: -"
            self.humid_label.text = "습도: -"
            self.rain_label.text = "강수: -"
            self.sky_label.text = "하늘상태: -"
            self.status_label.text = '날씨 정보를 불러오는데 실패했습니다.'
            self.status_label.text_color = (0, 0, 0, 1)

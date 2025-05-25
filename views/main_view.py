import os, sys
# 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.font_manager import get_font_name

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from models.weather_model import WeatherModel
from models.gps_model import GPSModel
from models.pace_model import PaceModel
from models.marathon_model import MarathonModel

from views.marathon_view import MarathonView
from views.weather_view import WeatherView
from views.pace_view import PaceView

from controllers.marathon_controller import MarathonController
from controllers.weather_controller import WeatherController
from controllers.gps_controller import GPSController
from controllers.pace_controller import PaceController


class MainView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # ScreenManager
        self.sm = ScreenManager()

        # Models
        self.marathon_model = MarathonModel()
        self.weather_model = WeatherModel()
        self.gps_model = GPSModel()
        self.pace_model = PaceModel()

        # Views
        self.marathon_view = MarathonView(name='marathon')
        self.weather_view = WeatherView(name='weather')
        self.pace_view = PaceView(name='pace')

        # Controllers
        self.marathon_controller = MarathonController(self.marathon_model, self.marathon_view)
        self.weather_controller = WeatherController(self.weather_model, self.weather_view)
        self.gps_controller = GPSController(self.gps_model, self.weather_view, self.weather_model)
        self.pace_controller = PaceController(self.pace_model, self.pace_view)

        # View와 Controller 연결
        self.marathon_view.controller = self.marathon_controller
        self.weather_view.controller = self.weather_controller
        self.pace_view.controller = self.pace_controller

        # ScreenManager에 View 추가
        self.sm.add_widget(self.marathon_view)
        self.sm.add_widget(self.weather_view)
        self.sm.add_widget(self.pace_view)

        # 메인 레이아웃에 ScreenManager 추가
        self.add_widget(self.sm)

        # 하단 네비게이션 바
        self.nav_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=5,
            padding=5
        )

        # 버튼 생성 (Kivy 기본 Button)
        self.marathon_btn = Button(
            text='마라톤',
            background_color=(0.1, 0.5, 0.9, 1),  # 메인 블루
            color=(1, 1, 1, 1),
            font_name=get_font_name(),
            size_hint_x=1
        )
        self.weather_btn = Button(
            text='날씨',
            background_color=(0.1, 0.5, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name=get_font_name(),
            size_hint_x=1
        )
        self.pace_btn = Button(
            text='페이스',
            background_color=(0.1, 0.5, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name=get_font_name(),
            size_hint_x=1
        )

        # 버튼 클릭 이벤트
        self.marathon_btn.bind(on_release=lambda x: self.switch_screen('marathon'))
        self.weather_btn.bind(on_release=lambda x: self.switch_screen('weather'))
        self.pace_btn.bind(on_release=lambda x: self.switch_screen('pace'))

        # 버튼 추가
        self.nav_bar.add_widget(self.marathon_btn)
        self.nav_bar.add_widget(self.weather_btn)
        self.nav_bar.add_widget(self.pace_btn)

        # 네비게이션 바 추가
        self.add_widget(self.nav_bar)

    def switch_screen(self, screen_name):
        self.sm.current = screen_name

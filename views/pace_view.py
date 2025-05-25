from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from views.base_view import BaseView
from utils.font_manager import get_font_name

class PaceView(BaseView):
    theme_primary_color = (0.1, 0.47, 0.82, 1)  # #1976D2
    theme_subtle_color = (0.89, 0.95, 0.99, 1)  # #E3F2FD

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._submit_callback = None
        self.controller = None

    def set_submit_callback(self, callback):
        self._submit_callback = callback

    def setup_ui(self):
        self.tab_panel = self.create_widget(TabbedPanel,
            do_default_tab=False,
            tab_pos='top_left',
            tab_width=200,
            background_color=self.theme_subtle_color,
            tab_height=50
        )

        input_tab = self.create_widget(TabbedPanelItem, text='입력')
        input_layout = self.create_boxlayout(orientation='vertical', padding=10, spacing=10)

        distance_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        distance_label = self.create_label(text='목표 거리 (km)', size_hint_x=0.3)
        self.distance_input = self.create_textinput(hint_text='목표 거리 (km)', multiline=False, size_hint_x=0.7)
        distance_layout.add_widget(distance_label)
        distance_layout.add_widget(self.distance_input)

        week_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        week_label = self.create_label(text='목표 주', size_hint_x=0.3)
        self.week_input = self.create_textinput(hint_text='주단위 입력', multiline=False, size_hint_x=0.7)
        week_layout.add_widget(week_label)
        week_layout.add_widget(self.week_input)

        goal_time_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        goal_time_label = self.create_label(text='목표 시간', size_hint_x=0.3)
        goal_time_input_layout = self.create_boxlayout(orientation='horizontal', size_hint_x=0.7)
        self.goal_time_hour_input = self.create_textinput(hint_text='시간', multiline=False, size_hint_x=0.5)
        self.goal_time_min_input = self.create_textinput(hint_text='분', multiline=False, size_hint_x=0.5)
        goal_time_input_layout.add_widget(self.goal_time_hour_input)
        goal_time_input_layout.add_widget(self.goal_time_min_input)
        goal_time_layout.add_widget(goal_time_label)
        goal_time_layout.add_widget(goal_time_input_layout)

        pace_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        pace_label = self.create_label(text='현재 페이스', size_hint_x=0.3)
        pace_input_layout = self.create_boxlayout(orientation='horizontal', size_hint_x=0.7)
        self.pace_min_input = self.create_textinput(hint_text='분', multiline=False, size_hint_x=0.5)
        self.pace_sec_input = self.create_textinput(hint_text='초', multiline=False, size_hint_x=0.5)
        pace_input_layout.add_widget(self.pace_min_input)
        pace_input_layout.add_widget(self.pace_sec_input)
        pace_layout.add_widget(pace_label)
        pace_layout.add_widget(pace_input_layout)

        max_distance_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        max_distance_label = self.create_label(text='최장 거리 (km)', size_hint_x=0.3)
        self.max_distance_input = self.create_textinput(hint_text='최장 거리 (km)', multiline=False, size_hint_x=0.7)
        max_distance_layout.add_widget(max_distance_label)
        max_distance_layout.add_widget(self.max_distance_input)

        level_layout = self.create_boxlayout(orientation='horizontal', size_hint_y=None, height=50)
        level_label = self.create_label(text='달리기 레벨:', size_hint_x=0.3)
        self.level_spinner = self.create_spinner(text='달리기 레벨 선택', values=('초급', '중급', '상급'), size_hint_x=0.7)
        level_layout.add_widget(level_label)
        level_layout.add_widget(self.level_spinner)

        self.level_desc_label = self.create_label(text='', size_hint_y=None, height=100)
        self.submit_button = self.create_button(text='훈련 계획 생성', size_hint_y=None, height=50)

        for widget in [self.distance_input, self.week_input, self.goal_time_hour_input,
                       self.goal_time_min_input, self.pace_min_input, self.pace_sec_input,
                       self.max_distance_input]:
            widget.background_color = self.theme_subtle_color
            widget.foreground_color = (0, 0, 0, 1)
            widget.cursor_color = self.theme_primary_color
            widget.font_name = get_font_name()

        self.submit_button.background_color = self.theme_primary_color
        self.submit_button.color = (1, 1, 1, 1)
        self.submit_button.font_name = get_font_name()

        self.level_spinner.background_color = self.theme_subtle_color
        self.level_spinner.font_name = get_font_name()

        self.level_desc_label.color = (0, 0, 0, 1)
        self.level_desc_label.font_name = get_font_name()

        input_layout.add_widget(distance_layout)
        input_layout.add_widget(week_layout)
        input_layout.add_widget(goal_time_layout)
        input_layout.add_widget(pace_layout)
        input_layout.add_widget(max_distance_layout)
        input_layout.add_widget(level_layout)
        input_layout.add_widget(self.level_desc_label)
        input_layout.add_widget(self.submit_button)
        input_tab.add_widget(input_layout)

        result_tab = self.create_widget(TabbedPanelItem, text='훈련 계획')
        self.result_layout = self.create_boxlayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, None))
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        result_scroll = self.create_widget(ScrollView, size_hint=(1, 1))
        result_scroll.add_widget(self.result_layout)
        result_tab.add_widget(result_scroll)

        self.tab_panel.add_widget(input_tab)
        self.tab_panel.add_widget(result_tab)
        self.layout.add_widget(self.tab_panel)

        self.level_spinner.bind(text=self.on_level_select)
        self.submit_button.bind(on_press=self.on_submit)

    def on_level_select(self, spinner, text):
        descriptions = {
            '초급': '풀코스 마라톤 완주경험 없음',
            '중급': '풀코스 마라톤 완주 경험 1회 이상',
            '상급': '풀코스 마라톤 완주 경험 다수'
        }
        self.level_desc_label.text = descriptions.get(text, '')

    
    def update_display(self, api_response):
        self.result_layout.clear_widgets()

        try:
            training_table = api_response.get("training_table", [])

            if not training_table:
                self.result_layout.add_widget(Label(text="데이터 없음", font_name=get_font_name()))
                return

            columns = ['주차', '월', '화', '수', '목', '금', '토', '일', '주간 거리']

            row_data = []
            for i, week in enumerate(training_table, start=1):
                row = [str(week.get("주차 #", i))]
                for day in ['월', '화', '수', '목', '금', '토', '일']:
                    row.append(week.get(day, "-"))
                row.append(str(week.get("주간 거리", "-")))
                row_data.append(tuple(row))

            table = MDDataTable(
                size_hint=(1, None),
                column_data=[(col, dp(30)) for col in columns],
                row_data=row_data,
                elevation=2
            )
            table.height = dp(40) * (len(row_data) + 1)
            self.result_layout.add_widget(table)

        except Exception as e:
            self.show_error(f"데이터 처리 오류: {str(e)}")



    def on_submit(self, instance):
        try:
            self.level_desc_label.text = "" #텍스트 초기화
            # 입력값 수집
            distance = self.distance_input.text
            week = self.week_input.text
            goal_hour = self.goal_time_hour_input.text
            goal_min = self.goal_time_min_input.text
            pace_min = self.pace_min_input.text
            pace_sec = self.pace_sec_input.text
            max_distance = self.max_distance_input.text
            level = self.level_spinner.text

            if self.controller:
                data = self.controller.generate_plan(
                    distance, week, goal_hour, goal_min, pace_min, pace_sec, max_distance, level
                )
                if isinstance(data, dict) and "error" in data:
                    self.show_error(data["error"])
                else:
                    self.update_display(data)
                    self.show_popup("훈련 계획이 성공적으로 생성되었습니다!", duration=2.0)
            else:
                self.show_error("Controller가 연결되지 않았습니다.")

        except Exception as e:
            self.show_error(f"오류 발생: {str(e)}")

    def show_error(self, msg):
        self.level_desc_label.text = f"[오류] {msg}"
        self.level_desc_label.color = (1,1,1,1) #white

    def show_popup(self, message, duration=1.0):
        popup_layout = self.create_boxlayout(orientation='vertical', padding=10, spacing=10)
        label = Label(
            text=message,
            font_name=get_font_name(),
            halign="center",
            valign="middle"
        )
        label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        popup = Popup(title='알림', content=popup_layout, size_hint=(0.7, 0.4), auto_dismiss=True)
        popup_layout.add_widget(label)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), duration)

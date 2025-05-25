from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from views.base_view import BaseView
from utils.font_manager import get_font_name

class MarathonView(BaseView):
    theme_primary_color = (0.1, 0.47, 0.82, 1)  # #1976D2
    theme_bg_color = (0.98, 0.98, 0.98, 1)      # #FAFAFA
    theme_subtle_color = (0.89, 0.95, 0.99, 1)  # #E3F2FD

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = None
        self.search_button_callback = None

    def setup_ui(self):
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        # 검색 영역
        self.search_card = MDCard(
            orientation='horizontal',
            padding=10,
            size_hint=(1, None),
            height=dp(60),
            md_bg_color=self.theme_bg_color,
            radius=[10,]
        )

        common_input_style = {
            "size_hint_x": 0.4,
            "size_hint_y": None,
            "height": dp(40),
            "font_name": get_font_name(),
            "background_color": self.theme_subtle_color,
            "foreground_color": (0, 0, 0, 1),
            "cursor_color": self.theme_primary_color,
            "halign": "center",
            "multiline": False,
            "padding_y": (dp(12), dp(12))  # 상하 중앙 정렬
        }

        self.year_input = TextInput(
            hint_text='연도 (예: 2025)',
            **common_input_style
        )

        self.month_input = TextInput(
            hint_text='월 (예: 5)',
            **common_input_style
        )

        self.search_button = MDRaisedButton(
            text='검색',
            md_bg_color=self.theme_primary_color,
            text_color=(1, 1, 1, 1),
            font_name=get_font_name(),
            size_hint_x=0.2,
            size_hint_y=None,
            height=dp(40)  # 연도/월과 동일한 높이
        )
        self.search_button.bind(on_press=self._on_search_button_press)

        self.search_card.add_widget(self.year_input)
        self.search_card.add_widget(self.month_input)
        self.search_card.add_widget(self.search_button)

        self.main_layout.add_widget(self.search_card)

        # 결과 테이블 영역
        self.table_scroll = ScrollView(size_hint=(1, 1))
        self.main_layout.add_widget(self.table_scroll)

        self.no_data_label = MDLabel(
            text="데이터 없음",
            halign="center",
            theme_text_color="Custom",
            text_color=self.theme_primary_color,
            font_name=get_font_name(),
            font_style="H6"
        )
        self.table_scroll.add_widget(self.no_data_label)

        self.layout.add_widget(self.main_layout)  # BaseView의 layout에 main_layout 추가

    def _on_search_button_press(self, instance):
        if self.controller:
            year = self.year_input.text
            month = self.month_input.text
            self.controller.search_marathons(year,month)

    def set_search_button_callback(self, callback):
        self.search_button_callback = callback

    def update_table(self, data, columns):
        self.table_scroll.clear_widgets()

        if not data:
            self.no_data_label.text = "데이터 없음"
            self.table_scroll.add_widget(self.no_data_label)
            return

        table = MDDataTable(
            size_hint=(1, None),
            column_data=[(col, dp(30)) for col in columns],
            row_data=[tuple(str(item.get(col, "-")) for col in columns) for item in data],
            elevation=2
        )

        table.height = dp(40) * (len(data) + 1)
        self.table_scroll.add_widget(table)

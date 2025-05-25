from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivy.graphics import Color, Rectangle

from utils.font_manager import get_font_name

# 한글 Spinner 옵션 처리 클래스
class KoreanSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', 'NanumGothic')
        super().__init__(**kwargs)

class BorderedLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', get_font_name())
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)  # 회색 테두리
            self.border_rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size
class BaseView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.setup_ui()
        self.add_widget(self._layout)

    @property
    def layout(self):
        return self._layout

    def create_widget(self, widget_class, **kwargs):
        if issubclass(widget_class, (Label, Button, TextInput, Spinner, TabbedPanelItem)):
            kwargs.setdefault('font_name', 'NanumGothic')
        if issubclass(widget_class, Spinner):
            kwargs.setdefault('option_cls', KoreanSpinnerOption)
        return widget_class(**kwargs)

    def create_label(self, **kwargs):
        kwargs.setdefault('font_name', get_font_name())
        kwargs.setdefault('font_size', '15sp')
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'top')
        kwargs.setdefault('size_hint_y', None)

        label = self.create_widget(Label, **kwargs)

        # ✅ 줄바꿈 + 높이 자동 조정
        label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )

        return label

    def create_wrapped_label(self, text, font_size='15sp', width='150'):
        label = self.create_label(
        text=text,
        font_size=font_size,
        size_hint_y=None,
        size_hint_x=None,
        width=width,  # 🔴 고정 폭이 있어야 text_size 계산이 가능
        halign='left',
        valign='top',
        color=(0, 0, 0, 1)
        )
        label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        return label
    
    
    def create_button(self, **kwargs):
        return self.create_widget(Button, **kwargs)

    def create_textinput(self, **kwargs):
        return self.create_widget(TextInput, **kwargs)

    def create_spinner(self, **kwargs):
        return self.create_widget(Spinner, **kwargs)

    def create_boxlayout(self, **kwargs):
        return self.create_widget(BoxLayout, **kwargs)

    def create_gridlayout(self, **kwargs):
        return self.create_widget(GridLayout, **kwargs)

    def create_scrollable_table_from_json(self, json_data: list, columns: list):
        """
        JSON 리스트 데이터를 기반으로 표 테이블을 만들고,
        흰색 배경 MDCard로 감싸서 ScrollView로 반환합니다.

        :param json_data: [{'주차':1, '월':'5km', ..., '주간_거리':20}, ...]
        :param columns: ['주차', '월', '화', '수', '목', '금', '토', '일', '주간_거리']
        :return: MDCard containing Scrollable Grid Table
        """

        # 1. 표 내부 레이아웃
        table = GridLayout(
            cols=len(columns),
            spacing=5,
            size_hint=(None, None),
            padding=5
        )
        table.bind(minimum_width=table.setter('width'), minimum_height=table.setter('height'))

        # 2. 헤더 생성 (BorderedLabel로 변경)
        for col in columns:
            header = BorderedLabel(text=col, font_size='15sp', size_hint=(None, None), size=(150, 40))
            table.add_widget(header)

        # 3. 각 행의 셀 생성 (BorderedLabel로 변경)
        for row in json_data:
            for col in columns:
                value = str(row.get(col, "-"))
                label = BorderedLabel(text=value, size_hint=(None, None), size=(150, 40))
                table.add_widget(label)

        # 4. ScrollView로 감싸기 (양방향 스크롤)
        scrollview = ScrollView(do_scroll_x=True, do_scroll_y=True, size_hint=(1, 1))
        scrollview.add_widget(table)

        # 5. 흰 배경 MDCard로 감싸기
        card = MDCard(
            size_hint=(1, None),
            height=500,  # 필요 시 동적으로 조정 가능
            padding=10,
            md_bg_color=(1, 1, 1, 1)  # ✅ 흰색 배경
        )
        card.add_widget(scrollview)

        return card

    def setup_ui(self):
        raise NotImplementedError("하위 클래스에서 반드시 구현해야 합니다.")

    def update_display(self, data):
        raise NotImplementedError("하위 클래스에서 반드시 구현해야 합니다.")
    

from kivymd.uix.button import MDFlatButton
from kivy.uix.button import Button
from utils.font_manager import get_font_name

def create_md_button(text, on_release=None):
    btn = MDFlatButton(
        text=text,
        text_color='white',
        md_bg_color=(0.1, 0.5, 0.9, 1),
        size_hint_x=1,
        halign='center',
        theme_text_color='Custom',
        font_name=get_font_name()
    )
    if on_release:
        btn.bind(on_release=on_release)
    return btn

def create_nav_button(text, on_release=None):
    btn = Button(
        text=text,
        background_color=(0.1, 0.5, 0.9, 1),  # 메인 블루 색상
        color=(1, 1, 1, 1),                   # 흰색 텍스트
        font_name=get_font_name(),
        size_hint_x=1,
        size_hint_y=1
    )
    if on_release:
        btn.bind(on_release=on_release)
    return btn
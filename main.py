from kivymd.app import MDApp
from views.main_view import MainView
from kivymd.theming import ThemeManager
from utils.font_manager import get_font_name

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.accent_hue = "600"
        self.theme_cls.theme_style = "Light"


        self.theme_cls.font_styles.update({
            "H1": [get_font_name(), 96, False, 0.0],
            "H2": [get_font_name(), 60, False, 0.0],
            "H3": [get_font_name(), 48, False, 0.0],
            "H4": [get_font_name(), 34, False, 0.0],
            "H5": [get_font_name(), 24, False, 0.0],
            "H6": [get_font_name(), 20, False, 0.0],
            "Subtitle1": [get_font_name(), 16, False, 0.0],
            "Subtitle2": [get_font_name(), 14, False, 0.0],
            "Body1": [get_font_name(), 16, False, 0.0],
            "Body2": [get_font_name(), 14, False, 0.0],
            "Button": [get_font_name(), 14, True, 1.25],
            "Caption": [get_font_name(), 12, False, 0.4],
            "Overline": [get_font_name(), 10, True, 1.5],
        })
        return MainView()

if __name__ == '__main__':
    MainApp().run()

# font_manager.py
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FALLBACK_FONT = 'Roboto'
DEFAULT_FONT = 'NanumGothic'
EMOJI_FONT = 'NotoColorEmoji-Regular.ttf'
EMOJI_FONT_NAME = 'EmojiFont'  # 등록 이름

FONT_FILE = 'NanumGothic.ttf'
_current_font = DEFAULT_FONT

def setup_fonts():
    global _current_font
    try:
        font_paths = [
            os.path.join(sys._MEIPASS, 'assets', 'fonts') if hasattr(sys, '_MEIPASS') else None,
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts'),
            os.path.join(os.path.dirname(__file__), '..', 'fonts'),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts'))
        ]

        font_path = None
        for path in font_paths:
            if path and os.path.exists(os.path.join(path, FONT_FILE)):
                font_path = path
                break
        if not font_path:
            raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {FONT_FILE}")

        resource_add_path(font_path)
        LabelBase.register(name=DEFAULT_FONT, fn_regular=FONT_FILE)
        LabelBase.register(name=EMOJI_FONT_NAME, fn_regular=EMOJI_FONT)
        _current_font = DEFAULT_FONT
        logger.info(f"폰트 설정 완료: {_current_font}, 이모지 폰트: {EMOJI_FONT_NAME}")

    except Exception as e:
        logger.error(f"폰트 설정 중 오류 발생: {str(e)}")
        _current_font = FALLBACK_FONT
        logger.warning(f"기본 폰트로 대체: {_current_font}")

def get_font_name():
    return _current_font

def get_emoji_font_name():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'NotoColorEmoji-Regular.ttf'))



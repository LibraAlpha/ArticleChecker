import time

import gradio as gr
from modules.extract_text import get_image_text
from modules.img_sim import calculate_ssim
from modules.text_processor import SeneitiveWordDetector
from modules.ui import create_ui

detector = SeneitiveWordDetector()

sensitive_image_list = []


def get_senstive_words_from_image(image):
    return detector.detect_sensitive_text(get_image_text(image))


def create_demo():
    with gr.Blocks(analytics_enabled=False, title='Asset Review') as demo:
        interfaces = []
        assert_review_interface = create_ui()
        interfaces += [(assert_review_interface, "Asset Review", "Asset Review")]

    for interface, label, ifid in interfaces:
        interface.render()

    return demo


def webui():
    demo = create_demo()
    demo.launch()


if __name__ == '__main__':
    webui()

import time

import gradio as gr
from modules.extract_text import get_image_text
from modules.text_processor import SeneitiveWordDetector

detector = SeneitiveWordDetector()

sensitive_image_list = []

def image_table():
    code = f"""<!-- {time.time()}-->
    <table id='images'>
        <thead>
            <tr>
                <th><abbr title="待审核图片素材">素材</abbr></th>
                <th>素材链接</th>
                <th><abbr title="检测到的敏感词">敏感词检测结果</abbr></th>
                <th><abbr title="操作">操作</abbr></th>
            </tr>
        </thead>
        <tbody>
    """

    for image in sensitive_image_list:
        image



def create_ui():
    with gr.Blocks() as ui:
        with gr.Tabs(elem_id='article_checker') as tabs:
            with gr.TabItem("敏感图片审核"):
                with gr.Row(elem_id='article_checker_top'):
                    load_button = gr.Button(value="加载待审核图片", variant="primary")

                    html = ""

                    html = """
                    <span style="color: var(--primary-400);">
                        加载所有待审核图片
                    </span>
                    """


            with gr.TabItem("已过滤图片"):

            with gr.TabItem("文案敏感词检测"):



def main():
    with gr.Blocks() as page:
        image_input = gr.Image(label='图片文字提取')
        image_submit = gr.Button('提取图片文字')
        image_output = gr.Textbox(label='图片内文字')
        image_submit.click(fn=get_image_text, inputs=image_input, outputs=image_output, api_name='get_image_text')

        text_input = gr.Textbox(label='文案敏感词识别')
        text_submit = gr.Button('识别')
        text_output = gr.Textbox(label='敏感词列表')
        text_submit.click(fn=detector.detect_sensitive_text, inputs=text_input, outputs=text_output)
        page.queue()
    page.launch(share=True)


if __name__ == '__main__':
    main()

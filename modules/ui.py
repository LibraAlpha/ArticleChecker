import time
import gradio as gr
from modules.text_processor import SensitiveWordDetector
from modules.extract_text import get_image_text
from modules.img_sim import calculate_ssim

sensitive_image_list = []
detector = SensitiveWordDetector()

def get_senstive_words_from_image(image):
    return detector.detect_sensitive_text(get_image_text(image))


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
    # for image in sensitive_image_list:


def create_ui():
    with gr.Blocks() as ui:
        with gr.Tabs(elem_id='assert_review') as tabs:
            with gr.TabItem("待审核图片列表"):
                with gr.Row(elem_id='assert_review_top'):
                    load_button_check = gr.Button(label="加载待审核图片", variant="primary", value='加载')

                    html = """
                    <span style="color: var(--primary-400);">
                        加载所有待审核图片
                    </span>
                    """
                    info = gr.HTML(html)
                    sensitive_image_table = gr.HTML(lambda: image_table())

            with gr.TabItem("黑名单素材列表"):
                with gr.Row(elem_id='assert_review_blacklist_top'):
                    load_button_filter = gr.Button(label="加载黑名单素材列表", variant="primary", value='加载')
                    html = """

                    """

            with gr.TabItem("文案敏感词检测"):
                with gr.Row():
                    image_input = gr.Image(label='图片敏感词识别')
                    image_submit = gr.Button('识别')
                    image_text_output = gr.Textbox(label='敏感词识别结果', lines=8)
                    image_submit.click(
                        fn=get_senstive_words_from_image,
                        inputs=image_input,
                        outputs=image_text_output,
                    )
                with gr.Row():
                    text_input = gr.Textbox(label='文案敏感词识别', lines=8)
                    text_submit = gr.Button('文案识别')
                    text_output = gr.Textbox(label='敏感词识别结果', lines=8)
                    text_submit.click(
                        fn=detector.detect_sensitive_text,
                        inputs=text_input,
                        outputs=text_output,
                    )

            with gr.TabItem("图片相似度判断"):
                with gr.Row():
                    image_sim_input_1 = gr.Image(label="图片A")
                    image_sim_input_2 = gr.Image(label="图片B")
                image_sim_submit_btn = gr.Button("计算图片相似度")
                ssim_output = gr.Textbox(label="相似度计算结果")
                image_sim_submit_btn.click(
                    fn=calculate_ssim,
                    inputs=[image_sim_input_1, image_sim_input_2],
                    outputs=ssim_output,
                )

    return ui

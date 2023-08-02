import os.path
import time
import gradio as gr
import gradio.routes

import modules.scripts
from modules.extract_text import get_image_text
from modules.img_sim import calculate_ssim
from modules.sensitive_word_detector import SensitiveWordDetector
from modules.sensitive_words_tools import find_sensitive_word, add_sensitive_word, remove

import html
from modules.paths_internal import javascript_path
import modules.shared as shared

sensitive_asset_list = []
detector = SensitiveWordDetector()


def webpath(script_file):
    if script_file.startswith(javascript_path):
        web_path = os.path.join(javascript_path, script_file).replace("\\", '/')
    else:
        web_path = os.path.abspath(script_file)

    return f'file={web_path}'


def javascript_html():
    script_js_ui = os.path.join(javascript_path, 'ui.js')

    head = f'<script type="text/javascript" src="{webpath(script_js_ui)}"></script>\n'

    # for script in javascript_path:
    #     head +=

    return head


def css_html():
    head = ""

    def stylesheet(fn):
        return f'<link rel="stylesheet" property="stylesheet" href="{webpath(fn)}">'

    for cssfile in modules.scripts.list_files_with_name("style.css"):
        if not os.path.isfile(cssfile):
            continue
        head += stylesheet(cssfile)

    return head


def reload_scripts():
    js = javascript_html()
    css = css_html()

    def template_response(*args, **kwargs):
        res = shared.GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{js}</head>'.encode('utf8'))
        res.body = res.body.replace(b'</body>', f'{css}</body>'.encode('utf8'))
        res.init_headers()
        return res

    gradio.routes.templates.TemplateResponse = template_response


if not hasattr(shared, 'GradioTemplateResponseOriginal'):
    shared.GradioTemplateResponseOriginal = gradio.routes.templates.TemplateResponse


def get_senstive_words_from_image(image):
    return detector.detect_sensitive_text(get_image_text(image))


def remove_word_from_list(word):
    detector.delete(word)


def reload_sensitive_list():
    detector.reload()


def asset_table():
    asset_code = f"""<!-- {time.time()}-->
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
    for asset in sensitive_asset_list:
        asset_code += f"""
        <tr>
            <td><img src={asset.url}></td>
            <td></td>
            <td></td>
            <td><button onclick="add_to_blacklist(this, {asset.url})"></td>
        <tr>
        """
    asset_code += """
        </tbody>        
    </table>
    """
    return asset_code


def word_table():
    code = f"""
    <table id='sensitive_words'>
        <thead>
            <tr>
                <th>敏感词</th>
                <th>操作</th>                
            </tr>
        </thead>        
        <tbody>
    """

    for word in detector.sensitive_word_list:
        code += f"""
            <tr>
                <td>{word}<td>
                <td><button onclick="del_sensitive_word(this, '{word}')">删除</button></td>                
            <tr>
        """
    code += """
        </tbody>        
    </table>
    """
    return code


def fnPlaceHolder():
    return "Get Response"


def create_ui():
    reload_scripts()

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
                    sensitive_image_table = gr.HTML(lambda: asset_table())

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
            with gr.TabItem('敏感词列表'):
                with gr.Row():
                    input_search = gr.Textbox(label='敏感词查询', placeholder='请输入希望查询的敏感词')
                    search_result_output = gr.Textbox(label='查询结果', placeholder='查询结果将在这里显示', lines=3)
                    search_btn = gr.Button("查询")
                    search_btn.click(
                        fn=find_sensitive_word,
                        inputs=[input_search],
                        outputs=search_result_output
                    )
                    reload_btn = gr.Button("重新加载")
                    reload_btn.click(
                        fn=reload_sensitive_list,
                        inputs=None,
                        outputs=None,
                    )
                with gr.Row():
                    word_insert = gr.Textbox(label='敏感词')
                    word_insert_btn = gr.Button("插入敏感词")
                    word_insert_btn.click(
                        fn=fnPlaceHolder,
                        inputs=[word_insert],
                        outputs=None
                    )
                    word_to_del = gr.Text(elem_id='word_to_del', visible=False)
                    del_word_btn = gr.Button(elem_id='del_sensitive_word_btn', visible=False)

                sensitive_word_table = gr.HTML(lambda: word_table())

                del_word_btn.click(
                    fn=remove,
                    inputs=word_to_del,
                    outputs=None,
                )
    return ui

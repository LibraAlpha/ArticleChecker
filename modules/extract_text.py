import configs.basics as Basic_Configs
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang="ch",
                det_model_dir=Basic_Configs.get_root_path() + '/models/ocr/inference/det/',
                rec_model_dir=Basic_Configs.get_root_path() + '/models/ocr/inference/rec/',
                cls_model_dir=Basic_Configs.get_root_path() + '/models/ocr/inference/cls/',
                use_gpu=False)  # need to run only once to download and load model into memory


def get_image_text(image):
    """
    image文件，ndarray格式
    :param image:
    :return:
    """
    result = ocr.ocr(image, cls=True)
    ret = ""
    for line in result:
        for content in line:
            ret += content[1][0] + " "
    return ret


def get_image_text_list(image):
    result = ocr.ocr(image, cls=True)
    ret = list()
    for line in result:
        for content in line:
            ret.append(content[1][0])
    return ret

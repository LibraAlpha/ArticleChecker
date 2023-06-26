import os

project_root_path = os.path.dirname((os.path.dirname((os.path.realpath(__file__)))))

javascript_path = os.path.join(project_root_path, 'js')

css_path = os.path.join(project_root_path, 'css')

model_path_base = os.path.join(project_root_path, 'models')

model_path_ocr = os.path.join(model_path_base, 'ocr')



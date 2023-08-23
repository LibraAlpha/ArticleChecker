ArticleChecker:基于FastApi开发的素材审核工具

## Install Paddlepaddle
#### If you have CUDA 9 or CUDA 10 installed on your machine, please run the following command to install
python -m pip install paddlepaddle-gpu -i https://pypi.tuna.tsinghua.edu.cn/simple

If you have no available GPU on your machine, please run the following command to install the CPU version
python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple

## Install PaddleOCR Whl Package
pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+

### 人心繁杂，知人心者，万事迎刃而解，不知人心者，万事皆为碍难

### configs: 项目配置相关
### models: 图片文字提取所需的模型文件
### modules/api: 接口部分代码，配置ip,端口后，启动api.py
### modules/db: 数据库以及redis操作相关
### modules/video: extract.py，图片文字提取模块；blur.py:图片整体高斯模糊
### modules/sensitive_word_detector:敏感词检测




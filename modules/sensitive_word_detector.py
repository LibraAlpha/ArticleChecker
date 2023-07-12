import base64
from configs import basics as basic_config
from modules.tools import read_large_file
from modules.sensitive_words_tools import load_all


class TireNode(object):
    def __init__(self):
        self.children = {}
        self.value = ""
        self.is_end = False


class SensitiveWordDetector(object):
    """
    敏感词检测,逐字符扫描，采用tire树结构处理字符匹配
    """
    def __init__(self):
        super(SensitiveWordDetector, self).__init__()
        self.sensitive_word_list = set()
        self.root = TireNode()
        try:
            self.load_from_db()
        except Exception as e:
            self.load_from_res_file()
        finally:
            self.build_tire(self.sensitive_word_list)

    def reload(self):
        self.sensitive_word_list = set()
        self.root = TireNode()
        try:
            self.load_from_db()
        except Exception as e:
            self.load_from_res_file()
        finally:
            self.rebuild()

    def load_from_res_file(self, blacklist_filePath=basic_config.get_root_path() + "/res/blacklist.txt"):
        """
        加载敏感词
        :param blacklist_filePath:敏感词文件，每行一个敏感词
        :return:
        """
        for word in read_large_file(blacklist_filePath):
            self.sensitive_word_list.add(word.strip())

    def load_from_db(self):
        self.sensitive_word_list = load_all()
        return

    def delete(self, word):
        if word in self.sensitive_word_list:
            self.sensitive_word_list.remove(word)
        self._delete_recursive(self.root, word, 0)

    def _delete_recursive(self, node: TireNode, word, index):
        if index == len(word):
            if node.is_end:
                node.is_end = False
            return

        char = word[index]
        if char not in node.children:
            return

        child = node.children[char]
        self._delete_recursive(child, word, index + 1)

        if not child.is_end and not child.children:
            del node.children[char]

    def insert_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TireNode()
                node.value = char
            node = node.children[char]
        node.is_end = True

    def build_tire(self, sensitive_words):
        for word in sensitive_words:
            self.insert_word(word)

    def detect_sensitive_text(self, text):
        sensitive_word_list = list()
        sensitive_word = ""
        node = self.root

        for char in text:
            if char in ('&', '', '*', '-', '+', '%', '~', '·', '!', '#'):
                continue
            if char in node.children:
                sensitive_word += char
                node = node.children[char]
                if node.is_end:
                    sensitive_word_list.append(sensitive_word)
                    sensitive_word = ""
                    node = self.root
            elif char in self.root.children:
                sensitive_word = char
                node = self.root.children[char]

        return sensitive_word_list

    def rebuild(self):
        self.build_tire(self.sensitive_word_list)

    @staticmethod
    def detect_sensitive_words_from_image(image):
        return detect_sensitive_text(get_image_text(image))

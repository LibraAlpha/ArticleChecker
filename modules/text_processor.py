from configs import basics as Basic_Configs
from modules.tools import read_large_file
import base64


class TireNode(object):
    def __init__(self):
        self.children = {}
        self.value = ""
        self.is_end = False


class SeneitiveWordDetector(object):
    """
    敏感词检测
    逐字符扫描
    """

    def __init__(self):
        super(SeneitiveWordDetector, self).__init__()
        self.sensitive_word_list = set()
        self.root = TireNode()
        self.load_sensitive_words()
        self.build_tire(self.sensitive_word_list)

    def load_sensitive_words(self, blacklist_filePath=Basic_Configs.get_root_path() + "/res/blacklist.txt"):
        """
        加载敏感词
        :param blacklist_filePath:敏感词文件，每行一个敏感词
        :return:
        """
        for line in read_large_file(blacklist_filePath):
            self.sensitive_word_list.add(line.strip())

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


if __name__ == '__main__':
    detector = SeneitiveWordDetector()
    for line in read_large_file(Basic_Configs.get_root_path() + "/res/sms_ban.txt"):
        print(base64.b64decode(line.strip('\n')).decode('utf-8').strip('\n'))

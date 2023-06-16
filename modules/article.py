class Article:
    def __init__(self, title, path, is_sensitive=True, is_checked=False):
        self.update_checker = None
        self.title = title
        self.path = path
        self.is_sensitive = is_sensitive
        self.is_checked = is_checked

    """
    # check_list
    # check_passed
    # 
    """


    def list_articles(self, is_sensitive=True, is_checked=False):
        """
        获取图片列表
        :return:
        """
        return



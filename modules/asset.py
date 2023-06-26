class Asset:
    def __init__(self, url, title, description, is_sensitive=True, is_checked=False):
        self.update_checker = None
        self.title = title
        self.description = description
        self.url = url
        self.is_sensitive = is_sensitive
        self.is_checked = is_checked

    """
    # check_list
    # check_passed
    # 
    """

    def load_assets(self):
        """
        从redis中加载黑名单列表
        :return:
        """

    def list_assets(self, is_sensitive=True, is_checked=False):
        """
        获取图片列表
        :return:
        """
        return

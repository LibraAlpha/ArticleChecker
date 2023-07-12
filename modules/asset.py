class Asset:
    def __init__(self, url, title, description, is_sensitive=True, is_checked=False):
        self.update_checker = None
        self.title = title
        self.description = description
        self.url = url
        self.is_sensitive = is_sensitive
        self.is_checked = is_checked

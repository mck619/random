class modifiedSoup(BeautifulSoup):
    def __init__(self, *args, **kwargs):
        self._url = None
        BeautifulSoup.__init__(self, *args, **kwargs)
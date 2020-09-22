from random import randint
from time import sleep


class userPage:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

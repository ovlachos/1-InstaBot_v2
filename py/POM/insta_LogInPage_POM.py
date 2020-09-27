from random import randint
from time import sleep
from POM import insta_topRibbon_POM as searchBoxMain
import auth


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class InstaLogIn:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        # self.driver.implicitly_wait(6)
        self.user = auth.username
        self.pw = auth.password

    def logIn(self):
        print(self.page.whichPageAmI())
        print(self.driver.session_id)
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
        except Exception as e:
            print(e)

        sleep(randint(2, 6))

        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.user)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

        sleep(4)

        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
            sleep(3)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        except Exception as e:
            print(e)

        sleep(5)
        return InstaMainPage(self.page)


class InstaMainPage:
    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.sb = searchBoxMain.SearchField(self.page)

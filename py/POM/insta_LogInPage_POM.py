import auth


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class InstaLogIn:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.user = auth.username
        self.pw = auth.password

    def logIn(self):
        from time import sleep
        from random import randint
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
        except Exception as e:
            print(e)

        sleep(randint(2, 6))

        try:
            self.driver.find_element_by_xpath("//button[contains(text(),'Accept')]").click()
        except Exception as e:
            print(e)

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
        from POM import insta_topRibbon_POM as topRibbon
        self.page = webPage
        self.driver = self.page.driver
        self.topRibbon_SearchField = topRibbon.SearchField(self.page)
        self.topRibbon_myAccount = topRibbon.AccountTab(self.page)

# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class InstaLogIn:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def logIn(self, user, pswd):
        from time import sleep
        from random import randint
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
        except Exception as e:
            print(e)

        sleep(randint(2, 6))

        try:
            self.page.getPageElement_tryHard("//button[contains(text(),'Accept')]").click()
        except Exception as e:
            print(e)

        self.page.getPageElement_tryHard("//input[@name=\"username\"]").send_keys(user)
        self.page.getPageElement_tryHard("//input[@name=\"password\"]").send_keys(pswd)
        self.page.getPageElement_tryHard('//button[@type="submit"]').click()

        sleep(4)

        try:
            self.page.getPageElement_tryHard("//button[contains(text(), 'Not Now')]").click()
            sleep(2)
            self.page.getPageElement_tryHard("//button[contains(text(), 'Not Now')]").click()
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

# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method
from time import sleep


class InstaID:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    url_USERNAMEtoID = 'https://commentpicker.com/instagram-user-id.php'
    url_IDtoUSERNAME = 'https://commentpicker.com/instagram-username.php'
    xpaths = {
        "cookies": "//button[@id='ez-accept-all']"
    }

    def getUserID(self, username):
        self.navigateTo(self.url_USERNAMEtoID)
        try:
            self.page.getPageElement_tryHard(self.xpaths['cookies']).click()
        except Exception as e:
            print(e)
        ID_userNameInputField = self.page.getPageElement_tryHard("//input[@id='instagram-username']")
        ID_get_button = self.page.getPageElement_tryHard("//button[@id='get-user-id-button']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ID_get_button)

        ID_userNameInputField.send_keys(username)

        ID_get_button.click()
        sleep(2)
        ID_result_box = self.page.getPageElement_tryHard("//div[@class='result-box__highlight']")
        return ID_result_box.text

    def getUserName(self, userID):
        self.navigateTo(self.url_IDtoUSERNAME)
        try:
            self.page.getPageElement_tryHard(self.xpaths['cookies']).click()
        except Exception as e:
            print(e)

        Username_IDinputField = self.page.getPageElement_tryHard("//input[@id='instagram-userid']")
        Username_get_button = self.page.getPageElement_tryHard("//button[@id='get-username-button']")
        self.driver.execute_script("arguments[0].scrollIntoView();", Username_get_button)

        Username_IDinputField.send_keys(userID)

        Username_get_button.click()
        Username_result_box = self.page.getPageElement_tryHard("//div[@class='result-box__highlight']//a")
        return Username_result_box.text

    def researchUsernameChange(self, username):
        return self.getUserName(self.getUserID(username))

    def navigateTo(self, url):
        self.driver.get(url)

    def leave(self):
        self.driver.quit()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class InstaID:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(4)

    url_USERNAMEtoID = 'https://commentpicker.com/instagram-user-id.php'
    url_IDtoUSERNAME = 'https://commentpicker.com/instagram-username.php'

    def getUserID(self, username):
        self.navigateTo(self.url_USERNAMEtoID)
        try:
            self.driver.find_element_by_xpath("//button[@id='ez-all-cookies']").click()
        except Exception as e:
            print(e)
        ID_userNameInputField = self.driver.find_element_by_xpath("//input[@id='instagram-username']")
        ID_get_button = self.driver.find_element_by_xpath("//button[@id='get-user-id-button']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ID_get_button)

        ID_userNameInputField.send_keys(username)

        ID_get_button.click()
        ID_result_box = self.driver.find_element_by_xpath("//div[@class='result-box__highlight']")
        return ID_result_box.text

    def getUserName(self, userID):
        self.navigateTo(self.url_IDtoUSERNAME)
        try:
            self.driver.find_element_by_xpath("//button[@id='ez-all-cookies']").click()
        except Exception as e:
            print(e)

        Username_IDinputField = self.driver.find_element_by_xpath("//input[@id='instagram-userid']")
        Username_get_button = self.driver.find_element_by_xpath("//button[@id='get-username-button']")
        self.driver.execute_script("arguments[0].scrollIntoView();", Username_get_button)

        Username_IDinputField.send_keys(userID)

        Username_get_button.click()
        Username_result_box = self.driver.find_element_by_xpath("//div[@class='result-box__highlight']//a")
        return Username_result_box.text

    def researchUsernameChange(self, username):
        return self.getUserName(self.getUserID(username))

    def navigateTo(self, url):
        self.driver.get(url)

    def leave(self):
        self.driver.quit()

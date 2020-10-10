from random import randint
from time import sleep


class Post:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.location = ""
        self.datePosted = ""
        self.usersCommented = []

    def like_post(self):
        try:
            sleep(randint(2, 6))
            try:
                # If it's a picture
                like_button = self.driver.find_element_by_xpath(
                    "//button[@class='wpO6b ']//*[contains(@aria-label,'ike')]/..")
            except:
                # If it's a video
                like_button = self.driver.find_element_by_xpath(
                    "//button[@class='wpO6b ']//*[contains(@aria-label,'ike')]/..")

            buttonStatus = like_button.find_element_by_class_name('_8-yf5 ').get_attribute('aria-label')
            if buttonStatus == 'Like':
                self.driver.execute_script("arguments[0].click();", like_button)
                sleep(2)

        except Exception as e:
            print(e)
            sleep(2)

    def close_post(self):
        try:
            sleep(1)
            self.driver.find_element_by_xpath("//*[@aria-label='Close']").click()
        except Exception as e:
            print(e)

    def getListOfUsersWhoLiked(self):
        outList = []
        return outList

    def updatePostLocation(self):
        try:
            loc_elements = self.driver.find_elements_by_xpath("//a[contains(@href,'/explore/locations')]")
            self.location = loc_elements[0].text
            if len(loc_elements) > 1:
                self.location = loc_elements[1].text
        except Exception as e:
            print(e)

    def updatePostDateTime(self):
        try:
            dateElement = self.driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']")
            self.datePosted = dateElement.get_attribute('datetime')
        except Exception as e:
            print(e)

    def updateUsers_commented_underPost(self):
        try:
            elements = self.driver.find_elements_by_xpath(
                "//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
            for element in elements:
                self.usersCommented.append(element.text)

            self.usersCommented = list(dict.fromkeys(self.usersCommented))
        except Exception as e:
            print(e)

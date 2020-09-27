from random import randint
from time import sleep


class Post:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def like_a_post(self):
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
                # like_button.click()
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

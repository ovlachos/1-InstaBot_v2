from time import sleep
import sched, time

from selenium.webdriver.common.keys import Keys

s = sched.scheduler(time.time, time.sleep)

xpaths = {
    "stories": "//button[@role='menuitem']/div/span",
    "storiesPauseButton": "//button//*[contains(@aria-label,'Pause')]",
    "storiesPlayButton": "//button//*[contains(@aria-label,'Play')]",
    "storiesCloseButton": "//div//*[contains(@aria-label,'lose')]",
    "storyNoLongerAvailableText": "//div//*[contains(text(),'available')]",
    "nextStoryButton": "//div[@class='coreSpriteRightChevron']",

    "postCommentButton": "//button//*[@aria-label='Comment']",
    "postLikeButton": "//section[@class='ltpMr  Slqrh']//button//*[contains(@aria-label,'ike')]",
}


class HomePage:
    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

        sleep(5)
        self.driver.refresh()
        sleep(5)

        self.postNumber = 0
        self.posts = self.page.getPageElements_tryHard(xpaths['postLikeButton'])

    def scrollNextPostIntoView(self):
        sleep(1)
        try:
            self.posts = self.page.getPageElements_tryHard(xpaths['postLikeButton'])

            if self.posts:
                self.driver.execute_script("arguments[0].scrollIntoView();", self.posts[self.postNumber])
                self.postNumber += 1

        except Exception as e:
            print(f'Navigating to post number {self.postNumber} failed for home page: {e}')
            if "stale" in e.msg:
                self.driver.refresh()

    def likeCurrentPost(self):
        sleep(1)
        try:
            post = self.posts[self.postNumber]
            like_button = None

            if post:
                try:
                    # self.driver.execute_script("arguments[0].scrollIntoView();", post)
                    like_button = self.posts[self.postNumber]
                except Exception as e:
                    print(e)
                    print('Could not find like button!')

                buttonStatus = like_button.get_attribute('aria-label')
                if buttonStatus == 'Like':
                    like_button.click()

                    sleep(2)

                    return True

            return False

        except Exception as e:
            print(f'Liking current post [number {self.postNumber}] failed for home page: {e}')
            if "stale" in e.msg:
                self.driver.refresh()

    def startWatchingStories(self, n):
        try:
            sleep(1)

            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

            sleep(2)

            # Click on first story
            firstStory = self.page.getPageElements_tryHard(xpaths['stories'])
            firstStory[0].click()

            sleep(3)

            if self.busyWatchingStories():
                for i in range(n):
                    s.enter(7, 1, self.storyUnavailable)

                s.run()

            self.stopWatchingStories()

        except Exception as e:
            print(f'Watching stories failed for home page: {e}')
            if "stale" in e.msg:
                self.driver.refresh()

    def stopWatchingStories(self):
        if self.busyWatchingStories():
            try:
                closeButton = self.page.getPageElement_tryHard(xpaths['storiesCloseButton'])

                if closeButton:
                    closeButton.click()

            except Exception as e:
                print(f'Watching stories stop! failed for home page: {e}')
                if "stale" in e.msg:
                    self.driver.refresh()

    def busyWatchingStories(self):
        try:
            closeButton = self.page.getPageElement_tryHard(xpaths['storiesCloseButton'])
            if closeButton:
                return True
        except Exception as e:
            return False

    def storyUnavailable(self):

        print("Checking if story available...")

        try:
            storyUnavailable = self.page.getPageElement_tryHard(xpaths['storyNoLongerAvailableText'])

            if storyUnavailable:
                sleep(2)
                nextButton = self.page.getPageElement_tryHard(xpaths['nextStoryButton'])
                nextButton.click()

        except:
            storyUnavailable = None

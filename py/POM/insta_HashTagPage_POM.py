# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method
from time import sleep

xpaths = {
    "postCount": "//div[@class='WSpok']//span[@class='g47SY ']",
    "hashTag": "//div[@class='WSpok']//h1[@class='_7UhW9       fKFbl yUEEX   KV-D4          uL8Hv         ']",
    "posts": "//div[@class='v1Nh3 kIKUG  _bz0w']//a",  # 'Most Recent' posts start after the top 9 posts
}


class HashTagPage:
    def __init__(self, webPage, hashtag):
        self.page = webPage
        self.driver = self.page.driver
        self.hashtag = hashtag

    def getPostCount(self):
        try:
            return self.page.getPageElement_tryHard(xpaths['postCount']).text.replace(',', '')
        except Exception as e:
            return None

    def navigateTo_X_mostRecentPosts(self, numberX):
        from POM import insta_post_POM as post
        numberX = numberX + 9  # offset by 9 to skip the 9 top liked posts at the top of the page
        try:
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            posts = self.driver.find_elements_by_xpath(xpaths['posts'])
            if len(posts) > 0 and len(posts) > numberX:
                self.driver.execute_script("arguments[0].scrollIntoView();", posts[numberX])
                self.driver.execute_script("arguments[0].click();", posts[numberX])
        except Exception as e:
            print(e)
            print('Opening post number {} failed'.format(numberX))
        return post.Post(self.page)

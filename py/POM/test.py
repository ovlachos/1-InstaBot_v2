from time import sleep

from POM import webPage as wp
from POM import insta_LogInPage_POM as login
from POM import insta_topRibbon_POM as ribbon

page1 = wp.WebPage()
page1.whichPageAmI()

logInPage = login.InstaLogIn(page1)

mainPage = logInPage.logIn()
mainPage.page.whichPageAmI()

myAccount = ribbon.AccountTab(page1)
field = ribbon.SearchField(page1)
field.navigateToUserPageThroughSearch("rrose___selavy")
field.page.whichPageAmI()
field.navigateToHashTagPageThroughSearch('streetphoto')
# count = field.getHashTagPostCountThroughSearch('streetwear')

myAccount.navigateToOwnProfile()
myAccount.logOut()

page1.driver.quit()

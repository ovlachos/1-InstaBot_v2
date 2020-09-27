from time import sleep

from POM import webPage as wp
from POM import insta_LogInPage_POM as login
from POM import insta_topRibbon_POM as ribbon
from POM import insta_userPage_POM as up
from POM import insta_post as post

page1 = wp.WebPage()
page1.whichPageAmI()

logInPage = login.InstaLogIn(page1)

mainPage = logInPage.logIn()
mainPage.page.whichPageAmI()

myAccount = ribbon.AccountTab(page1)
field = ribbon.SearchField(page1)

sleep(2)

field.navigateToUserPageThroughSearch('katsikis')
akis = up.userPage(page1, 'katsikis')
sleep(2)

myAccount.logOut()
page1.driver.quit()

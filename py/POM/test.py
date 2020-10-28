from time import sleep
from POM import webPage as wp
from POM import insta_LogInPage_POM as login
import FileHandlerBot as fb
import InstaBotV2 as IB

# page1 = wp.WebPage()
mineBot = IB.InstaBot(True)
mineBot.logIn()
mineBot.theGame()
mineBot.shutDown()

print('plop')

# logInPage = login.InstaLogIn(page1)
# mainPage = logInPage.logIn()
#
# akis = mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch('katsikis')
#
# # print('User {} {}'.format(akis.userName, akis.get_profileTypeDescription()))
# nums = [x for x in range(10)]
#
# for n in nums:
#     po = akis.navigateTo_X_latestPost(n)
#     sleep(1)
#     po.like_post()
#     po.close_post()
#     sleep(1)
#
# mainPage.topRibbon_myAccount.logOut()
# page1.driver.quit()

# do your check “ element in set(alist) “

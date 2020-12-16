import pandas
import InstaBotV2
from time import sleep

bot = InstaBotV2.InstaBot()
bot.getBrowser()
bot.logIn()

user = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch('mar_ia.karamani_91')
sleep(1)
user = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch('erie.tta_sl')
sleep(1)
user = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch('katsikis')

# Bot Cleanup Lists ~ Keep for later as a self-cleanup check?
# myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
# myFollowing = myPage.getFollowingList()
#
# theFrame = bot.fileHandler.CSV_getFrameFromCSVfile('theList_1_fileCSV')
#
# theFilteredFrameKeep = theFrame[(theFrame[theFrame.columns[3]] == 'keep') & (theFrame.iloc[:, 7].isnull())]
# theKeepList = theFilteredFrameKeep[theFilteredFrameKeep.columns[1]].tolist()
#
# theFilteredFrameDrop = theFrame[(theFrame[theFrame.columns[3]] == 'drop')]
# theDropList = theFilteredFrameDrop[theFilteredFrameDrop.columns[1]].tolist()
#
# everyList = theFrame[theFrame.columns[1]].tolist()
#
# myDroppedFollowing = [x for x in myFollowing if x in theDropList]
# myKeptFollowing = [x for x in myFollowing if x in theKeepList]
# everyone = [x for x in myFollowing if x in everyList]
#
# df = pandas.DataFrame(myDroppedFollowing, columns=['Dropped_Following'])
# df0 = pandas.DataFrame(myKeptFollowing, columns=['Kept_Following'])
# df1 = pandas.DataFrame(everyone, columns=['Everyone In the Game!'])
#
# df.to_csv('/Users/cortomaltese/Google Drive/10 Projects/1 InstaBot_v2/Output/Games_Output/Dropped_Following.csv',
#           index=False, encoding='utf-8')
#
# df0.to_csv('/Users/cortomaltese/Google Drive/10 Projects/1 InstaBot_v2/Output/Games_Output/Kept_Following.csv',
#            index=False, encoding='utf-8')
#
# df1.to_csv('/Users/cortomaltese/Google Drive/10 Projects/1 InstaBot_v2/Output/Games_Output/cleanUpFollowing1.csv',
#            index=False, encoding='utf-8')

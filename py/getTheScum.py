import InstaFameBot
import auth
import pandas as pd
import sys
from datetime import datetime
from os import path
import have_I_been_played

if len(sys.argv) > 1:
    hdLess = sys.argv[1]
else:
    hdLess = False

InstaFameBot.log.error('\n\n')
InstaFameBot.log.error('MyStats - Scum Report')
now = datetime.now()
date_ = now.strftime("%Y_%m_%d")
helper = InstaFameBot.HelperBot()
whiteList = pd.read_csv(InstaFameBot.file_paths.theScumWhiteListCSV)['userWhiteList'].tolist()
whiteList = list(dict.fromkeys(whiteList))

newPaths = [InstaFameBot.file_paths.theScum + 'theScum' + date_ + '.csv',
            InstaFameBot.file_paths.myStats + 'myFollowers' + date_ + '.csv',
            InstaFameBot.file_paths.myStats + 'myFollow_ing' + date_ + '.csv']

oldPaths = [InstaFameBot.file_paths.theScumMainCSV,
            InstaFameBot.file_paths.myStats_FolowersCSV,
            InstaFameBot.file_paths.myStats_FollowingCSV]

alternativeScumCSV = InstaFameBot.file_paths.theScumMainCSV[:-4] + '_alternative.csv'

# Get new list/row of scum
bot = InstaFameBot.InstaBot(auth.username, auth.password, headless=hdLess)
bot.tH_logIn()
theList = bot.t1_getListOfUsers_thatDontFollowBack(auth.username)

if len(theList) == 3:
    InstaFameBot.log.error('{0}: Got the stats on all three categories'.format(str(path.basename(__file__))[:-3]))

if bot.tooManyActionsBreakCode not in theList:

    theList[0] = [x for x in theList[0] if x not in whiteList]

    for ii in range(0, len(theList)):
        newFrame = pd.DataFrame(theList[ii])
        newFrame.columns = [date_]
        newFrame.to_csv(newPaths[ii], index=False, encoding='utf-8')
        newRow = [date_, len(theList[ii])] + theList[ii]

        oldFrame = pd.read_csv(oldPaths[ii])

        try:
            newMainFrame = helper.addNewRow_toDataFrame(oldFrame, newRow)
            newMainFrame.to_csv(oldPaths[ii], index=False, encoding='utf-8')
        except Exception as e:
            print(e)
        InstaFameBot.log.error('{0}: updated stats for {1}'.format(str(path.basename(__file__))[:-3],
                                                                   newPaths[ii][
                                                                   -int(-1.5 * (ii ** 2) + 5.5 * ii + 21):]))
    try:
        played = have_I_been_played.haveIbeenPlayed()
        InstaFameBot.log.error(
            '{0}: {1} {2}'.format(str(path.basename(__file__))[:-3], 'have_I_been_played? ', played))
    except Exception as e:
        InstaFameBot.log.error(
            '{0}: Could not run {1} because: {2}'.format(str(path.basename(__file__))[:-3], 'have_I_been_played', e))

bot.tH_logOut()
bot.tH_close_browser()

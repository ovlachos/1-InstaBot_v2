import InstaFameBot
import auth
from time import sleep
import datetime
from os import path

InstaFameBot.log.error('\n\n')
numberOfUsersToProcess = 80
passes = 2
bot = InstaFameBot.InstaBot(auth.username, auth.password)

for innn in reversed(range(0, passes)):
    InstaFameBot.log.error(
        '{0}: Building the List 1 for the pass {1} out of {2}'.format(str(path.basename(__file__))[:-3],
                                                                      (passes - innn), (passes)))
    bot.tH_logIn()
    answer = bot.t2_getList_1(numberOfUsersToProcess)

    if answer == bot.tooManyActionsBreakCode:
        break

    bot.tH_logOut()

    print('-- Now asleep')
    for five_minute in reversed(range(0, 3)):
        sleep(5 * 60)
        print('{0} -- Still {1} minutes of sleep left'.format(datetime.datetime.today(), str(five_minute * 5)))
    print('-- Now awake')

bot.tH_escapeSequence()
InstaFameBot.log.error('\n ~~~ L-1 END ~~~ \n\n')

import InstaFameBot
import pandas as pd
import auth
from time import sleep

bot = InstaFameBot.InstaBot(auth.username, auth.password)
bot.tH_logIn()
passes = 5
for innn in reversed(range(0, passes)):
    bot.t2_getHashtagFollowership(10)
    bot.tH_logOut()
    bot.tH_close_browser()

    print('-- Now asleep')
    for five_minute in reversed(range(0, 6)):
        sleep(5 * 60)
        print('{0} -- Still {1} minutes of sleep left'.format(datetime.datetime.today(), str(five_minute * 5)))
    print('-- Now awake')

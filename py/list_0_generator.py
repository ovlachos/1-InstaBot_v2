import InstaFameBot
import auth
from os import path
from time import sleep

InstaFameBot.log.error('\n\n')
InstaFameBot.log.error('{0}: Building the List 0'.format(str(path.basename(__file__))[:-3]))

bot = InstaFameBot.InstaBot(auth.username, auth.password)
bot.tH_logIn()
answer = bot.t2_getList_0(10)
bot.tH_logOut()
bot.tH_close_browser()

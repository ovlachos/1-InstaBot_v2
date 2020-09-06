import InstaFameBot as ib
import auth
from time import sleep

ib.log.error('\n\n')
ib.log.error('~~<>~~ Let the Game Begin')
gamingBot = ib.InstaBot(auth.username, auth.password)
gamingBot.tH_logIn()
gamingBot.t2_theGame(30)
print("~~<>~~ The Game is over")
gamingBot.tH_logOut()
gamingBot.tH_close_browser()

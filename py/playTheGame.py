import InstaBotV2 as ibV2
import sys

if len(sys.argv) > 1:
    hdLess = sys.argv[1]
else:
    hdLess = False

thebot = ibV2.InstaBot(hdLess)
thebot.logIn()
thebot.theGame(30)
thebot.shutDown()

# ib.log.error('\n\n')
# ib.log.error('~~<>~~ Let the Game Begin')
# gamingBot = ib.InstaBot(auth.username, auth.password, headless=hdLess)
# gamingBot.tH_logIn()
# gamingBot.t2_theGame(30)
# print("~~<>~~ The Game is over")
# gamingBot.tH_logOut()
# gamingBot.tH_close_browser()

import InstaFameBot
import auth

routerBot = InstaFameBot.InstaBot(auth.username, auth.password)
routerBot.tH_resetRouter()
routerBot.tH_close_browser()

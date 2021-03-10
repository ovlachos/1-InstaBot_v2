import InstaBotV2

bot = InstaBotV2.InstaBot()
bot.getBrowser()
bot.logIn()

theDailyResponse = bot.theGame_Service()

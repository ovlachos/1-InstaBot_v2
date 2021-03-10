import InstaBotV2

try:
    v2Bot = InstaBotV2.InstaBot(False)
    v2Bot.getBrowser()
    v2Bot.logIn()
    a = input()
except:
    v2Bot.shutDown()

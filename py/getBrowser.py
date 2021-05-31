import InstaBotV2

try:
    v2Bot = InstaBotV2.InstaBot(False)
    v2Bot.getBrowser()
    v2Bot.logIn()
    print('Ok now just waiting...')
    a = input()
except Exception as e:
    # v2Bot.shutDown()
    print(e)
    v2Bot.shutDown()

import InstaBotV2

bot = InstaBotV2.InstaBot()
bot.getBrowser()
bot.logIn()

# bot.memoryManager.readMemoryFileFromDrive()

theExtraResponse = bot.love_Service('extra', 1, 0.501)
if 'busted' in theExtraResponse:
    print("Busted!")

# bot.memoryManager.redistributeExtraLove()
# bot.memoryManager.writeMemoryFileToDrive()

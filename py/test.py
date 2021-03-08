import json
import os
from datetime import datetime, timedelta
import pandas as pd
import InstaBotV2
from time import sleep
from BotMemory import Users_M as UM

bot = InstaBotV2.InstaBot()
# bot.getBrowser()
# bot.logIn()

# theDailyResponse = bot.loveService('extra', 1, 0.01)


bot.memoryManager.readMemoryFileFromDrive()
memoryFile = bot.memoryManager.getMemoryFile()

for user in memoryFile:
    if user.dateUnFollowed_byMe == "" or user.dateUnFollowed_byMe == " ":
        print('yas!')
        user.dateUnFollowed_byMe = None
    else:
        print('boo')

# bot.memoryManager.writeMemoryFileToDrive()

import json
import os
from datetime import datetime, timedelta
import pandas
import InstaBotV2
from time import sleep
from BotMemory import Users_M as UM

bot = InstaBotV2.InstaBot()
bot.getBrowser()
bot.logIn()

theDailyResponse = bot.loveService(fileName='extra', percentageOfUsers=1, numberOfLikes=1)

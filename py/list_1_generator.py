import sys
import InstaBotV2
from random import randint
from time import sleep


def main():
    hdLess = False
    numberOfProfilesToProcess = 2

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            numberOfProfilesToProcess = int(sys.argv[2])
        except Exception as e:
            print(e)
    else:
        hdLess = False

    print([hdLess, type(hdLess), numberOfProfilesToProcess, type(numberOfProfilesToProcess)])
    sleepTime = randint((2 * 60), (20 * 60))
    sleep(sleepTime)
    print(f'Sleeping for {sleepTime / 60} minutes')

    bot = InstaBotV2.InstaBot(hdLess)
    bot.logIn()
    bot.list_getList_1(numberOfProfilesToProcess)
    # bot.shutDown()
    del bot


if __name__ == "__main__": main()

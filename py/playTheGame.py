import sys
import InstaBotV2 as ibV2
from time import sleep
from random import randint


def main():
    hdLess = False
    numberOfProfilesToProcess = 5

    if len(sys.argv) > 1:

        print(sys.argv)

        if sys.argv[1] == 'True':
            hdLess = True
        try:
            numberOfProfilesToProcess = int(sys.argv[2])
        except Exception as e:
            print(e)

    print([hdLess, type(hdLess), numberOfProfilesToProcess, type(numberOfProfilesToProcess)])

    sleepTime = randint((2 * 60), (20 * 60))
    sleep(sleepTime)
    print(f'Sleeping for {sleepTime / 60} minutes')

    theBot = ibV2.InstaBot(hdLess)
    theBot.logIn()
    theBot.theGame(numberOfProfilesToProcess)
    # theBot.shutDown()
    del theBot


if __name__ == "__main__": main()

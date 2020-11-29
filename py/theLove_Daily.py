import sys
import InstaBotV2
from random import randint
from time import sleep


def main():
    hdLess = False
    noOfLikesToGive = 1
    percentageOfUsersToCover = 0.501

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            noOfLikesToGive = int(sys.argv[2])
            percentageOfUsersToCover = float(sys.argv[3])
        except Exception as e:
            print(e)

    print([hdLess, type(hdLess), noOfLikesToGive, type(noOfLikesToGive), percentageOfUsersToCover,
           type(percentageOfUsersToCover)])

    sleepTime = randint((2 * 60), (20 * 60))
    sleep(sleepTime)
    print(f'Sleeping for {sleepTime / 60} minutes')

    v2Bot = InstaBotV2.InstaBot(hdLess)
    v2Bot.logIn()
    v2Bot.theLoveDaily('dailyLoveCSV', noOfLikesToGive, percentageOfUsersToCover)
    v2Bot.theLoveDaily('extraLoveCSV', noOfLikesToGive, 0.501)
    # v2Bot.shutDown()
    del v2Bot


if __name__ == "__main__": main()

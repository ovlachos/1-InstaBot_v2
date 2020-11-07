import sys
import InstaBotV2


def main():
    hdLess = False
    noOfLikesToGive = 1
    percentageOfUsersToCover = 0.40

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

    v2Bot = InstaBotV2.InstaBot(hdLess)
    v2Bot.logIn()
    v2Bot.theLoveDaily('dailyLoveCSV', noOfLikesToGive, percentageOfUsersToCover)
    v2Bot.theLoveDaily('extraLoveCSV', noOfLikesToGive, 1.0)
    v2Bot.shutDown()


if __name__ == "__main__": main()

import sys
import InstaBotV2 as ibV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 30

    if len(sys.argv) > 1:

        print(sys.argv)

        if sys.argv[1] == 'True':
            hdLess = True
        try:
            numberOfProfilesToProcess = int(sys.argv[2])
        except Exception as e:
            print(e)

    print([hdLess, type(hdLess), numberOfProfilesToProcess, type(numberOfProfilesToProcess)])

    theBot = ibV2.InstaBot(hdLess)
    theBot.logIn()
    theBot.theGame(numberOfProfilesToProcess)
    theBot.shutDown()


if __name__ == "__main__": main()

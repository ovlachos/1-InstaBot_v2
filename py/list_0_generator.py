import sys
import InstaBotV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 10

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

    bot = InstaBotV2.InstaBot(hdLess)
    bot.logIn()
    bot.list_getList_0(numberOfProfilesToProcess)
    # bot.shutDown()
    del bot


if __name__ == "__main__": main()

import InstaFameBot
import auth
import sys
import time
from os import path


def main(likesPerUser=1, hoursOfWait=0):
    start_time = time.time()
    if len(sys.argv) > 1:
        likesPerUser = int(sys.argv[1])
        if len(sys.argv) > 2:
            hoursOfWait = int(sys.argv[2])

    InstaFameBot.log.error('\n\n')
    InstaFameBot.log.error('{0}: -- -- gearing up for the Love Daily'.format(str(path.basename(__file__))[:-3]))

    InstaFameBot.log.error(
        '{0}: --I will be giving out {1} likes per user today mylord'.format(str(path.basename(__file__))[:-3],
                                                                             likesPerUser))
    bot = InstaFameBot.InstaBot(auth.username, auth.password)

    # args: likesPerUser, True/False, File path
    bot.tH_logIn()
    success = bot.t2_theLoveDaily(likesPerUser, percentageOfUsers=0.52)

    elapsed_time = time.time() - start_time
    InstaFameBot.log.error('{0} -- I gave out {1} likes per user today mylord'.format(success, likesPerUser))
    InstaFameBot.log.error('~~ TheLoveDay ~~ The time ellapsed was {} minutes'.format((elapsed_time / 60)))

    bot.tH_escapeSequence()


if __name__ == "__main__": main()

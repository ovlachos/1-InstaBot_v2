import hashTagEvaluation as hs
import time
from InstaFameBot import HelperBot as help


def main():
    # ~~~~~~~ The actual script ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    inputFilepaths_0 = hs.findAll_TXT_CSV_Files_pathsToList(hs.paths['input'])
    theHelp = help

    # Input Parameters
    intervalInSeconds = 60 * 45
    numberOfSamples = 0

    samples = True
    # samples = False

    # Input files
    photoName = 'syracuse_weddingPhoto'
    # photoName = 'vlachou'
    hs.log.error("\n\n")
    hs.log.error("Starting #tag sampling round for {0}".format(photoName))

    # Make sure you form the researchLists
    # before moving to the next step
    researchLists_not_Formed = True
    while researchLists_not_Formed:
        researchLists_not_Formed = hs.form_Hashtag_Research_List_final(photoName)

    if samples:
        # Get a number of Samples
        for i in range(0, numberOfSamples):
            start_time = time.time()
            hs.getSamples(photoName)
            end_time = time.time()
            timeMin = str(round(((end_time - start_time) / 60), 2))
            message = '{0} minutes elapsed on this round.'.format(timeMin)
            hs.log.error(message)
            hs.log.error('------------------------------------------\n')
            print(message)

            if numberOfSamples > 1:
                print('Going to bed for {0}'.format(intervalInSeconds))
                time.sleep(intervalInSeconds)
    else:
        hs.runHastagStats(photoName)


if __name__ == '__main__':
    main()

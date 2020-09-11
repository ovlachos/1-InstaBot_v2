import glob
import time
import os
import hashTagEvaluation as hs
from InstaFameBot import HelperBot as help


def main(photoName, numberOfSamples=1, samples=True):
    # ~~~~~~~ The actual script ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    # ~~~~~~~ ~~~~~~~   ~~~~~~~ ~~~~~~~
    inputFilepaths_0 = hs.findAll_TXT_CSV_Files_pathsToList(hs.paths['input'])
    theHelp = help

    # Input Parameters
    intervalInSeconds = 60 * 45

    # Input files
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
    pyPath = os.path.dirname(__file__)
    projectFolderPath = os.path.join(pyPath, '../')
    inputs = os.path.join(projectFolderPath, 'Inputs/')
    os.chdir(inputs)

    # create a list with all the .txt file paths
    paths = []
    for file in glob.glob("*hashtags.txt"):
        paths.append(inputs + file)
    paths.sort()
    if len(paths) > 0:
        f = open(paths[0], "r")
        argum = []
        for line in f:
            argum.append(line.strip('?\n'))

        if len(argum) > 2:
            if argum[2] == 'True':
                argum[2] = True
            elif argum[2] == 'False':
                argum[2] = False
            main(argum[0], int(argum[1]), samples=argum[2])
        else:
            main("photoName", numberOfSamples=1, samples=True)

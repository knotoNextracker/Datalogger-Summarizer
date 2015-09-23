from os import listdir
import os
from os.path import isfile, join
import time
import logging
import Check_Archives
import shutil

def main():
    logger = logging.getLogger("Summarizer_Loop")
    logger.info("----- Start Summarizer.py -----")

    def listToCSV(array_input):
        output = str(array_input[0])
        for i in range(1,len(array_input)):
            output += ',' + str(array_input[i])
        return output

    #Get list of .dat files in directory
    mypath = "\\\\10.10.1.150\das\Garnet"
    # mypath = "C:\Users\knotohamiprodjo\Desktop\py_data"
    logger.info( "Populating file list in " + mypath + "...")
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    onlydat = [ g for g in onlyfiles if "dat" in g ]

    #Get list of only accelerometer data files from onlydat
    onlybatt = [ h for h in onlydat if "AHRS" in h]

    #Remove RAW files
    noraw = [ j for j in onlybatt if not "raw" in j]
    only1696 = [ i for i in noraw if "1696" in i]
    only1697 = [i for i in noraw if "1697" in i]
    logger.info( "Checking if archive is up to date...")
    if not(Check_Archives.main(only1696 + only1697)):
        update_list = Check_Archives.main(only1696+only1697,return_list = True)
        numdataloggers = len(update_list) if len(update_list)>0 else len(only1696+only1697)
        logger.info(str(numdataloggers) + " files to summarize.")
        logger.debug("List of .dat files to update: %r" % update_list)
        logger.info("Predicted time to complete: " + str(0.26 * numdataloggers) + " seconds.")
        logger.info("Working...")
        #Create output and initialize headers
        outputFilename = "C:\Users\knotohamiprodjo\Desktop\py_dev\Summary.xlsx"
        archiveFilename = "C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx"
        try:
            os.remove(outputFilename)
            logger.debug("Removed %r" % outputFilename)
        except:
            logger.debug("Could not remove %r" % outputFilename)
            pass    

        #Go through all 1696 data and write to fout

        start_time = time.time()
        logger.info( "Begin datalogger summary...")

        import Datalogger_archiver
        Datalogger_archiver.main(outputFilename)

        try:
            os.remove(archiveFilename)
            logger.debug("Removed %r" % archiveFilename)
        except:
            logger.debug("Could not remove %r" % archiveFilename)
            pass
        shutil.copyfile(outputFilename, archiveFilename)
        logger.debug("Copied %r to %r" % (outputFilename,archiveFilename))

        logger.info( "Summary complete!")
        elapsed_time = time.time() - start_time
        logger.info( "Total Time: " + str(elapsed_time) + "seconds for " + str(numdataloggers) + " dataloggers.")
        logger.info("Total Time: " + str(elapsed_time) + "seconds for " + str(numdataloggers) + " dataloggers.")
        logger.info( str(elapsed_time / numdataloggers) + " seconds per file.")
        logger.info( "----- IMAGE CREATION -----")
        logger.info( "Beginning image creations Grapherizer.py...")
        import Grapherizer
        Grapherizer.main(update_list if len(update_list)>0 else only1696 + only1697)
        logger.info( "----- WIND SUMMARY -----")
        logger.info( "Beginning wind60min summary...")
        import Wind60
        Wind60.main()
        logger.info( "----- VIDEO FILES -----")
        logger.info( "Grabbing Video Files....")
        import Video_Sorter
        Video_Sorter.main(update_list)
    else:
        logger.info("Summary up to date, no updates required.")
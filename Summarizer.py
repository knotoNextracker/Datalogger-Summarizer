from os import listdir
import os
from os.path import isfile, join
import time
import logging
import Check_Archives
import shutil

def main():
    logging.getLogger(__name__)
    logging.info("Begin execution " + str(time.strftime("%a, %d %b %Y %H:%M:%S")))

    def listToCSV(array_input):
        output = str(array_input[0])
        for i in range(1,len(array_input)):
            output += ',' + str(array_input[i])
        return output

    #Get list of .dat files in directory
    mypath = "\\\\10.10.1.150\das\Garnet"
    # mypath = "C:\Users\knotohamiprodjo\Desktop\py_data"
    print "Populating file list in " + mypath + "..."
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    onlydat = [ g for g in onlyfiles if "dat" in g ]

    #Get list of only accelerometer data files from onlydat
    onlybatt = [ h for h in onlydat if "AHRS" in h]

    #Remove RAW files
    noraw = [ j for j in onlybatt if not "raw" in j]
    only1696 = [ i for i in noraw if "1696" in i]
    only1697 = [i for i in noraw if "1697" in i]
    print "Checking if archive is up to date..."
    if not(Check_Archives.main(only1696 + only1697)):
        videolist = Check_Archives.main(only1696+only1697,return_list = True)
        numdataloggers = len(noraw)
        logging.info(str(numdataloggers) + " files to summarize.")
        print str(len(only1696)) + " primary datalogger files."
        print str(len(only1697)) + " secondary datalogger files."
        print "Predicted time to complete: " + str(0.26 * numdataloggers) + " seconds."
        print "Working..."
        #Create output and initialize headers
        outputFilename = "C:\Users\knotohamiprodjo\Desktop\py_dev\Summary.xlsx"
        archiveFilename = "C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx"
        try:
            os.remove(outputFilename)
        except:
            pass    

        #Go through all 1696 data and write to fout

        start_time = time.time()
        print "Begin datalogger summary..."

        import Datalogger_archiver
        Datalogger_archiver.main(outputFilename)

        try:
            os.remove(archiveFilename)
        except:
            pass
        shutil.copyfile(outputFilename, archiveFilename)

        print "Summary complete!"
        elapsed_time = time.time() - start_time
        print "Total Time: " + str(elapsed_time) + "seconds for " + str(numdataloggers) + " dataloggers."
        logging.info("Total Time: " + str(elapsed_time) + "seconds for " + str(numdataloggers) + " dataloggers.")
        print str(elapsed_time / numdataloggers) + " seconds per file."
        print "----- IMAGE CREATION -----"
        print "Beginning image creations Grapherizer.py..."
        import Grapherizer
        Grapherizer.main()
        print "----- WIND SUMMARY -----"
        print "Beginning wind60min summary..."
        import Wind60
        Wind60.main()
        print "----- VIDEO FILES -----"
        print "Grabbing Video Files...."
        import Video_Sorter
        Video_Sorter.main(videolist)
    else:
        logging.info("Summary up to date, no updates required.")
        print "Summary up to date, no updates required."
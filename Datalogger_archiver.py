import os
import time
import getMax
import logging
from os.path import isfile, join
import pandas
import Check_Archives

def main(output_filename):
	logger = logging.getLogger("Summarizer_Loop")
	logger.info("----- Start Datalogger_Archiver -----")
	mypath = "\\\\10.10.1.150\das\Garnet"
	logger.info("Populating file list in " + mypath + "...")
	onlyfiles = [ f for f in os.listdir(mypath) if isfile(join(mypath,f)) ]

	onlydat = [ g for g in onlyfiles if "dat" in g ]

	#Get list of only accelerometer data files from onlydat
	onlybatt = [ h for h in onlydat if "AHRS" in h]

	#Remove RAW files
	noraw = [ j for j in onlybatt if not "raw" in j]
	only1696 = [ i for i in noraw if "1696" in i]
	only1697 = [i for i in noraw if "1697" in i]

	
	try:
		arc_path = 'C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx'
		arc_excel = pandas.read_excel(arc_path,sheetname = 'Sheet1')
		missing_files = Check_Archives.main(only1696+only1697 , return_list = True)
		filenames = arc_excel['Filename'].values.tolist()
		datetime_start = arc_excel['Start Time'].values.tolist()
		datetime_end = arc_excel['End Time'].values.tolist()
		hour_start = arc_excel['Hour Start'].values.tolist()
		maxWinds = arc_excel['Max Windsp (mph)'].values.tolist()
		maxaccs = arc_excel['Max Acc (g)'].values.tolist()
		maxdisps = arc_excel['Max Disp (cm)'].values.tolist()
		avgtrackerangles = arc_excel['Average Tracker Angle (+W/-E) (deg)'].values.tolist()
		event_durations = arc_excel['Event Duration'].values.tolist()
		timeperdatapoints = arc_excel['Time per Datapoint'].values.tolist()
		first_event_end = arc_excel['First Event End'].values.tolist()
	except:
		logger.info("No archive. Creating new file.")
		missing_files = only1696+only1697
		filenames = []
		datetime_start = []
		datetime_end = []
		hour_start = []
		maxWinds = []
		maxaccs = []
		maxdisps = []
		avgtrackerangles = []
		event_durations = []
		timeperdatapoints = []
		first_event_end = []
	logger.info("Opening .dat files...")
	for i in missing_files:
		logger.debug("Opening %r" % i)
		max_data = getMax.main(i)
		filenames.append(i)
		datetime_start.append(max_data[0])
		datetime_end.append(max_data[1])
		hour_start.append(max_data[2])
		maxWinds.append(max_data[3])
		maxaccs.append(max_data[4])
		maxdisps.append(max_data[5])
		avgtrackerangles.append(max_data[6])
		event_durations.append(max_data[7])
		timeperdatapoints.append(max_data[8])
		first_event_end.append(max_data[9])
	data = {
		'Filename':filenames,
		'Start Time':datetime_start,
		'End Time':datetime_end,
		'Hour Start':hour_start,
		'Max Windsp (mph)':maxWinds,
		'Max Acc (g)':maxaccs,
		'Max Disp (cm)':maxdisps,
		'Average Tracker Angle (+W/-E) (deg)':avgtrackerangles,
		'Event Duration':event_durations,
		'Time per Datapoint':timeperdatapoints,
		'First Event End': first_event_end
	}
	logger.info("Creating Dataframe")
	df = pandas.DataFrame(data)
	df = df[[
		'Filename',
		'Start Time',
		'End Time',
		'Hour Start',
		'Max Windsp (mph)',
		'Max Acc (g)',
		'Max Disp (cm)',
		'Average Tracker Angle (+W/-E) (deg)',
		'Event Duration',
		'Time per Datapoint',
		'First Event End'
		]]

	logger.info("Writing to Excel")
	writer = pandas.ExcelWriter(output_filename)

	df.to_excel(writer,'Sheet1',index = False)
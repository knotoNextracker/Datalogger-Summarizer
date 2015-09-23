import pandas
from time import strftime, strptime
import Event_Video_Getter
import logging
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')
module_name = 'Video_Sorter'

logging.getLogger(config.get('Logger','logger_name'))

def main(missing_files):
	logging.info("------ Starting Video_Sorter -----")
	excel_path = config.get('Paths','archive_path')
	logging.debug("Accessing excel path: %r" % excel_path)
	arc_excel = pandas.read_excel(excel_path,sheetname = 'Sheet1')
	# missing_files = ['CR6_1696_AHRS_2015_08_13_2058.dat',
	# 'CR6_1696_AHRS_2015_08_13_2117.dat',
	# 'CR6_1696_AHRS_2015_08_13_2143.dat',
	# 'CR6_1696_AHRS_2015_08_13_2148.dat']
	logging.info("Filtering filenames based on missing_files")
	filter_filename = [i in arc_excel['Filename'].values.tolist() for i in missing_files]
	df_filter_filename = arc_excel.iloc[filter_filename]
	disp_threshold = config.getfloat(module_name,'disp_threshold')
	filter_disp = [i>disp_threshold for i in df_filter_filename['Max Disp (cm)']]
	filtered_excel = df_filter_filename.iloc[filter_disp]
	if len(filtered_excel['Filename'])>0:
		logging.debug("Getting videos for the following excel sheets: %r" % filtered_excel['Filename'])
	else:
		logging.info("No video files to get!")

	for idx,fl in enumerate(filtered_excel['Filename']):
		start_time = strftime("%m%d%y%H%M%S",strptime(filtered_excel['Start Time'].iloc[idx],"%Y-%m-%d %H:%M:%S"))
		end_time = strftime("%m%d%y%H%M%S",strptime(filtered_excel['First Event End'].iloc[idx],"%Y-%m-%d %H:%M:%S"))
		logging.debug("Start Time: %r, End Time: %r" % (start_time,end_time))
		Event_Video_Getter.main(start_time,end_time)
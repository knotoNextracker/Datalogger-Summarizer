import pandas
from time import strftime, strptime
import Event_Video_Getter

def main(missing_files):
	excel_path = "C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx"
	arc_excel = pandas.read_excel(excel_path,sheetname = 'Sheet1')
	# missing_files = ['CR6_1696_AHRS_2015_08_13_2058.dat',
	# 'CR6_1696_AHRS_2015_08_13_2117.dat',
	# 'CR6_1696_AHRS_2015_08_13_2143.dat',
	# 'CR6_1696_AHRS_2015_08_13_2148.dat']

	filter_filename = [i in arc_excel['Filename'].values.tolist() for i in missing_files]
	df_filter_filename = arc_excel.iloc[filter_filename]
	filter_disp = [i>5 for i in df_filter_filename['Max Disp (cm)']]
	filtered_excel = df_filter_filename.iloc[filter_disp]

	for idx,fl in enumerate(filtered_excel['Filename']):
		start_time = strftime("%m%d%y%H%M%S",strptime(filtered_excel['Start Time'].iloc[idx],"%Y-%m-%d %H:%M:%S"))
		end_time = strftime("%m%d%y%H%M%S",strptime(filtered_excel['First Event End'].iloc[idx],"%Y-%m-%d %H:%M:%S"))
		Event_Video_Getter.main(start_time,end_time)
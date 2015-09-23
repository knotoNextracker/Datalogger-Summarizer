import requests
from time import strptime, strftime, sleep
import os
import datetime
from os.path import isfile, join
from os import listdir
import Check_Archives
import pandas
import logging

def main(event_start,event_end,pre_record_duration = 0, post_record_duration = 0):
	logger = logging.getLogger("Summarizer_Loop")
	logger.info("----- Start Event_Video_Getter -----")
	dt = datetime.datetime
	event_start = strptime(event_start,"%m%d%y%H%M%S")
	event_end = strptime(event_end, "%m%d%y%H%M%S")

	# if event_end in [ None , '' ,'None'] :
	# 	logger.info(No event_end time, waiting for datalogger update to determine event end')
	# 	for counter in range(0,6):
	# 		mypath = "\\\\10.10.1.150\das\Garnet"
	# 		# mypath = "C:\Users\knotohamiprodjo\Desktop\py_data"
	# 		print "Populating file list in " + mypath + "..."
	# 		onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	# 		onlydat = [ g for g in onlyfiles if "dat" in g ]

	# 		#Get list of only accelerometer data files from onlydat
	# 		onlybatt = [ h for h in onlydat if "AHRS" in h]

	# 		#Remove RAW files
	# 		noraw = [ j for j in onlybatt if not "raw" in j]
	# 		only1696 = [ i for i in noraw if "1696" in i]
	# 		only1697 = [i for i in noraw if "1697" in i]
	# 		if Check_Archives.main(only1696 + only1697):
	# 			logger.info(Waiting 5 min for event to end...')
	# 			sleep(60*5)
	# 		elif counter == 5:
	# 			logger.info(30 min elapsed, no datalogger update, shutting down video getter...')
	# 			return
	# 		else:
	# 			break
	# 	excel_path = "C:\Users\knotohamiprodjo\Desktop\py_dev\Summary.xlsx"
	# 	excel = pandas.read_excel(excel_path,sheetname = 'Sheet1')

	# 	for idx,val in excel['Start Time'].iteritems():
	# 		if str(val) != 'nan':
	# 			excel['Start Time'][idx] = dt.strptime(val,"%Y-%m-%d %H:%M")

	# 	for idx,val in excel['End Time'].iteritems():
	# 		if str(val) != 'nan':
	# 			excel['End Time'][idx] = dt.strptime(val,"%Y-%m-%d %H:%M")

	# 	excel[(excel['Start Time']>event_start)]

	login = ('admin','S01aR.P0w3R')
	logger.info('Connecting to webpage...')
	webpage = "http://172.16.203.4"
	r = requests.get(webpage + "/server/events/",auth = login)


	response = r.content
	def linkscrubber(content):
		def no_neg(neg_list):
			result = []
			for idx,val in enumerate(neg_list):
				if val < 0:
					result.append(99999)
				else:
					result.append(val)
			return result
		base_dir_start = content.find('Index of ')+9
		base_dir_end = content.find('<',base_dir_start)
		base_dir = content[base_dir_start:base_dir_end]
		months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		pre_start = content.find('<PRE>')
		pre_end = content.find('</PRE>')
		if pre_start == 0 or pre_end == 0:
			raise ValueError('Cannot find <PRE>')
		content = content[pre_start+5:pre_end]
		href = []
		last_changed = []
		isdir = []
		href_start = content.find("<A HREF=")+8
		href_end = content.find(">",href_start)
		tc_start = min(no_neg([content.find(k) for k in months]))
		tc_end = tc_start + 15
		while all([href_start > 7,href_end >= 0,tc_start>=0,0<tc_end<=len(content)]):
			last_changed.append(content[tc_start:tc_end])
			href.append(content[href_start:href_end])
			content = content[href_end:]
			href_start = content.find("<A HREF=")+8
			href_end = content.find(">",href_start)
			tc_start = min(no_neg([content.find(k) for k in months]))
			tc_end = tc_start + 15
		for idx,val in enumerate(href):
			if idx == 0 or idx == 1:
				href[idx] = ''
				last_changed[idx] = ''
				isdir.append('')
			elif '.' in val:
				href[idx] = val.replace(base_dir,'').replace('"','')
				try:
					str_time = strptime('15 ' + last_changed[idx],"%y %b %d %H:%M:%S")
				except:
					str_time = ''
				last_changed[idx] = str_time
				isdir.append(0)
			else:
				href[idx] = val.replace(base_dir,'').replace('"','')
				try:
					str_time = strptime('15 ' + last_changed[idx],"%y %b %d %H:%M:%S")
				except:
					str_time = ''
				last_changed[idx] = str_time
				isdir.append(1)
		return base_dir, href, last_changed, isdir

	base_dir, href, last_changed, isdir = linkscrubber(response)
	dirs = [href[idx] for idx,val in enumerate(isdir) if val == 1]

	# Open first level and get the base 3digit folders
	logger.info('Navigating directories...')
	r1 = requests.get(webpage + base_dir + '/' + dirs[0], auth = login)
	response1 = r1.content
	base_dir1, href1, last_changed1, isdir1 = linkscrubber(response1)
	dirs1 = [href1[idx] for idx,val in enumerate(isdir1) if val == 1]

	# Open next level and get folder separated events
	dirs2 = []
	video_filenames = []
	video_last_changed = []
	video_directories = []
	keep_going = True
	logger.info('Looking for files between %r and %r' % (strftime("%m/%d/%y %H:%M:%S",event_start),strftime("%m/%d/%y %H:%M:%S",event_end)))
	for path in reversed(dirs1):
		r2 = requests.get(webpage + base_dir1 + '/' + path, auth = login)
		response2 = r2.content
		base_dir2, href2, last_changed2, isdir2 = linkscrubber(response2)
		dirs2_a = [href2[idx] for idx,val in enumerate(isdir2) if val == 1]
		for foo in dirs2_a:
			dirs2.append(foo)

		for folder in reversed(dirs2):
			r3 = requests.get(webpage + base_dir2 + '/' + folder, auth = login)
			response3 = r3.content
			base_dir3, href3, last_changed3, isdir3 = linkscrubber(response3)
			files3 = [href3[idx] for idx,val in enumerate(isdir3) if val == 0 and href3[idx] != '']
			files3_last_changed = [last_changed3[idx] for idx,val in enumerate(isdir3) if val == 0 and href3[idx] != '']
			files3_paths = [base_dir3 + '/' + i for i in files3]
			for idx,val in enumerate(reversed(files3)):
				idx = -1 - idx
				if event_start < files3_last_changed[idx] < event_end and 'M' in files3[idx]:
					video_filenames.append(files3[idx])
					video_last_changed.append(files3_last_changed[idx])
					video_directories.append(files3_paths[idx])
				elif files3_last_changed[idx] < event_start:
					keep_going = False
					break
				else:
					pass
			if keep_going == False:
				break
		if keep_going == False:
			break

	logger.info("Downloading %r files..." % len(video_filenames))

	# Write files
	export_number = 1
	export_filename = strftime("%m%d%y%H%M%S",event_start)
	export_path = "C:\Users\knotohamiprodjo\Desktop\py_dev\Video_Files" + "\\" + export_filename
	if not os.path.exists(export_path) and len(video_filenames)>0:
		logger.info('CREATING DIRECTORY ' + export_path)
		os.makedirs(export_path)
		for directory in reversed(video_directories):

			video_file = webpage + directory
			logger.info("Downloading %r as %r ..." % (video_file,export_path + '/' + export_filename + '_' + str(export_number) + '.mxg'))

			with open(export_path + "\\" + export_filename + '_' + str(export_number) + '.mxg','wb') as handle:
				response = requests.get(video_file,auth = login, stream=True)

				if not response.ok:
					logger.info('ERROR IN DOWNLOAD')

				for block in response.iter_content(1024):
					handle.write(block)
				export_number += 1
				logger.info("Download Complete")
	elif len(video_filenames)==0:
		logger.info("No files to download!")
	elif not(os.path.exists(export_path)):
		logger.info("Directory already exists!")

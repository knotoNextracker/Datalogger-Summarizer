from os import listdir
import os
import numpy
from os.path import isfile, join
from numpy import genfromtxt
import matplotlib.dates as md
import datetime as dt
import pandas
import time
import logging

def main():
	def getTime(timestamp):
		return timestamp[11:17]

	# mypath = "C:\Users\knotohamiprodjo\Desktop\py_data\NEW"
	mypath = "\\\\10.10.1.150\das\Garnet"

	print "Populating file list in " + mypath + "..."
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	onlydat = [ g for g in onlyfiles if "dat" in g ]

	#Get list of only wind data files from onlydat
	onlywind = [ h for h in onlydat if "Wind60min" in h]

	numdataloggers = len(onlywind)
	logging.info(str(numdataloggers) + " files to summarize.")
	print str(len(onlywind)) + " Wind60min files."
	print "Working..."


	outputFilename = "C:\Users\knotohamiprodjo\Desktop\py_dev\WindSummary.csv"
	try:
	    os.remove(outputFilename)
	except:
	    pass    
	fout = open(outputFilename,"a")
	fout.write('DateTime,Time,Wind Speed, Wind Direction, Max Wind Speed Direction, Max Wind Speed, Max Wind Speed DateTime,Time')
	fout.write('\n')
	fout.write(',,mph,deg,deg,mph,,')
	fout.write('\n')


	for filename in onlywind:
		csv = pandas.read_csv(mypath + '\\' +  filename, header = 1, skiprows = [2,3,4,5]) #creates data frame
		result = [csv['TIMESTAMP'],map(getTime,csv['TIMESTAMP']),csv['WS_mph_S_WVT'],csv['WindDir_D1_WVT'],csv['WindDir_SD1_WVT'],csv['wind_sp_Max'],csv['wind_sp_TMx'],map(getTime,csv['wind_sp_TMx'])]
		if len(result[0])==0:
			pass
		else:
			output=[]
			for j in range(0,len(result[0])):
				for i in range(0,len(result)):
					if i == 0:
						output = []
						output = str(result[0][j])
					else:
						output += ',' + str(result[i][j])
				fout.write(output)
				fout.write('\n')
	fout.close()
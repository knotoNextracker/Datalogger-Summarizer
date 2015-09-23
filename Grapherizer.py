# Creates graphs from all datalogger files with the option to choose data options, animate or not, or overwrite
# should migrate this to graph only a single datalogfile....

from os import listdir
import os
import numpy
from os.path import isfile, join
from numpy import genfromtxt
import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
from myAnimate import myAnimate
#Get list of .dat files in directory
def get_inputs():
	output_format = str(raw_input('Which Data [Acc, Disp, Ang]: '))
	animateYN = str(raw_input('Animate? [Y/N]: '))
	overwriteYN = str(raw_input('Overwrite existing? [Y/N]: '))
	return [output_format,animateYN,overwriteYN]


def write_inputs():
	output_format = 'Disp'
	animateYN = 'N'
	overwriteYN = 'N'
	return [output_format,animateYN,overwriteYN]

def main(args=write_inputs()):
	output_format = args[0]
	animateYN = args[1]
	overwriteYN = args[2]
	images_made = 0
	animations_made = 0
	# datapath = "C:\Users\knotohamiprodjo\Desktop\py_data\NEW"
	datapath = "\\\\10.10.1.150\das\Garnet"
	exportpath = "C:\Users\knotohamiprodjo\Desktop\py_dev"
	print "Populating file lists..."
	dirs = [d for d in os.listdir(exportpath) if os.path.isdir(os.path.join(exportpath,d))]
	onlyfiles = [ f for f in listdir(datapath) if isfile(join(datapath,f)) ]
	onlydat = [ g for g in onlyfiles if "dat" in g ]

	#Get list of only accelerometer data files from onlydat
	onlybatt = [ h for h in onlydat if "AHRS" in h]

	#Remove RAW files
	noraw = [ j for j in onlybatt if not "raw" in j]

	#Split files of 1696 and 1697
	only1696 = [i for i in noraw if "1696" in i]
	only1697 = [i for i in noraw if "1697" in i]
	print 'Found ' + str(len(only1696)) + ' primary logs and ' + str(len(only1697)) + ' secondary logs.'

	#Get desired outputs and animation request
	print 'Working...'

	#Configure output format for future graph labels
	if output_format == 'Acc':
		output_format_label = 'Acc [g]'
	elif output_format == 'Disp':
		output_format_label = 'Disp [cm]'
	elif output_format == 'Ang':
		output_format_label = 'Ang [deg]'

	#Averages entire dataset and subtracts from dataset, returns adjusted dataset
	def offset(a):
		result = []
		average = numpy.average(a)
		for i in a:
			result.append(i-average)
		return result

	def totrackerangle(angle):
	    if angle > 0:
	        return  - (180 - angle)
	    else:
	        return  - (- 180 - angle)

	def convertanglelist(anglelist):
		output = []
		for i in anglelist:
			output.append(totrackerangle(i))
		return output

	#iterate through primary datalogger files
	for i in only1696:
		filename = i
		filedate = i[14:24]
		savepath = exportpath + '\\' + filedate + '\\' + output_format 
		filename_second = filename[0:7] + '7' + filename[8:] #generate secondary datalogger filename

		if not os.path.exists(savepath):
			print 'CREATING DIRECTORY ' + savepath
			os.makedirs(savepath)
		else:
			pass
		existfiles = [ a for a in listdir(savepath) if isfile(join(savepath,a)) ]
		if filename[:-4] + '_' + output_format + '.jpg' in existfiles and overwriteYN == 'N':

			try:
				only1697.pop(only1697.index(filename_second))
			except:
				pass
			pass
		else:
			csv = pandas.read_csv(datapath + '\\' +  filename,header = 1,skiprows = [2,3,4,5])
			
			if len(csv['TIMESTAMP'])<5:
				continue
			
			# Create and configure subplots
			fig,axes = plt.subplots(nrows=2,ncols=3)
			fig.set_size_inches(25,15)
			plt.tight_layout(pad=7, w_pad=7, h_pad=6)
			
			if output_format == 'Acc':
				axislim = [-.2,.2]
			elif output_format == 'Disp':
				axislim = [-2,2]
			elif output_format == 'Ang':
				axislim = [-35,35]

			windlim = [0,40]
			xfmt = md.DateFormatter('%H:%M:%S')

			# Configure xy data
			df_wind = csv[['wind_sp']]
			xdates = []

			for j in csv['TIMESTAMP']:
				try:
					xdates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f"))
				except:
					xdates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S"))

			x = md.date2num(xdates)

			if output_format == 'Acc':
				df_data = [offset(csv['XAcc_50m']),offset(csv['YAcc_50m']),offset(csv['ZAcc_50m'])]
				df_data1 = [offset(csv['XAcc_40m']),offset(csv['YAcc_40m']),offset(csv['ZAcc_40m'])]
				df_data2 = [offset(csv['XAcc_30m']),offset(csv['YAcc_30m']),offset(csv['ZAcc_30m'])]

			elif output_format == 'Disp':
				df_data = [offset(csv['XDisp_50m']),offset(csv['YDisp_50m']),offset(csv['ZDisp_50m'])]
				df_data1 = [offset(csv['XDisp_40m']),offset(csv['YDisp_40m']),offset(csv['ZDisp_40m'])]
				df_data2 = [offset(csv['XDisp_30m']),offset(csv['YDisp_30m']),offset(csv['ZDisp_30m'])]

			elif output_format == 'Ang':
				df_data = [convertanglelist(csv['trackerAngle_50m'])]
				df_data1 = [convertanglelist(csv['trackerAngle_40m'])]
				df_data2 = [convertanglelist(csv['trackerAngle_30m'])]
			# Plot primary acc or disp data 50m
			axes[0,0].xaxis.set_major_formatter(xfmt)
			if output_format == 'Ang':
				axes[0,0].plot(x,df_data[0])
			else:
				axes[0,0].plot(x, df_data[0],x,df_data[1],x,df_data[2],alpha=0.4)
			axes[0,0].set_ylabel(output_format_label)
			axes[0,0].set_ylim(axislim[0],axislim[1])
			axes[0,0].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
			axes[0,0].set_title(filename)
			# Plot twin wind data over same plot
			df_disp_twin = axes[0,0].twinx()
			df_disp_twin.xaxis.set_major_formatter(xfmt)
			df_disp_twin.set_ylabel('Wind [mph]')
			df_disp_twin.set_ylim(windlim[0],windlim[1])
			df_disp_twin.plot(x,df_wind,color='m')
			# Change legend based on desired output_format
			if output_format == 'Acc':
				axes[0,0].legend(['XAcc_50m','YAcc_50m','ZAcc_50m'])
			elif output_format == 'Disp':
				axes[0,0].legend(['XDisp_50m','YDisp_50m','ZDisp_50m'])
			elif output_format == 'Ang':
				axes[0,0].legend(['trackerAngle_50m'])

			# Plot primary acc or disp data 40m
			axes[0,1].xaxis.set_major_formatter(xfmt)
			if output_format == 'Ang':
				axes[0,1].plot(x,df_data1[0],x,df_data1[0])
			else:
				axes[0,1].plot(x, df_data1[0],x,df_data1[1],x,df_data1[2],alpha=0.4)
			axes[0,1].set_ylabel(output_format_label)
			axes[0,1].set_ylim(axislim[0],axislim[1])
			axes[0,1].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
			# Plot twin wind data over same plot
			df_disp_twin1 = axes[0,1].twinx()
			df_disp_twin1.xaxis.set_major_formatter(xfmt)
			df_disp_twin1.set_ylabel('Wind [mph]')
			df_disp_twin1.set_ylim(windlim[0],windlim[1])
			df_disp_twin1.plot(x,df_wind,color='m')
			# Change legend based on desired output_format
			if output_format == 'Acc':
				axes[0,1].legend(['XAcc_40m','YAcc_40m','ZAcc_40m'])
			elif output_format == 'Disp':
				axes[0,1].legend(['XDisp_40m','YDisp_40m','ZDisp_40m'])
			elif output_format == 'Ang':
				axes[0,1].legend(['trackerAngle_40m','trackerAngle_30m'])

			# Plot primary acc or disp data 30m
			if output_format == 'Ang':
				pass
			else:
				axes[0,2].xaxis.set_major_formatter(xfmt)
				axes[0,2].plot(x, df_data2[0],x,df_data2[1],x,df_data2[2],alpha=0.4)
				axes[0,2].set_ylabel(output_format_label)
				axes[0,2].set_ylim(axislim[0],axislim[1])
				axes[0,2].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
				# Plot twin wind data over same plot
				df_disp_twin2 = axes[0,2].twinx()
				df_disp_twin2.xaxis.set_major_formatter(xfmt)
				df_disp_twin2.set_ylabel('Wind [mph]')
				df_disp_twin2.set_ylim(windlim[0],windlim[1])
				df_disp_twin2.plot(x,df_wind,color='m')
				# Change legend based on desired output_format
				if output_format == 'Acc':
					axes[0,2].legend(['XAcc_30m','YAcc_30m','ZAcc_30m'])
				elif output_format == 'Disp':
					axes[0,2].legend(['XDisp_30m','YDisp_30m','ZDisp_30m'])

			# Try to plot secondary datalogger if exists/possible 
			try:
				csv2 = pandas.read_csv(datapath + '\\' + filename_second, header = 1, skiprows = [2,3,4,5])
				df_wind2 = csv2[['wind_sp']]
				if output_format == 'Acc':
					df_data3 = [offset(csv2['XAcc_20m']),offset(csv2['YAcc_20m']),offset(csv2['ZAcc_20m'])]
					df_data4 = [offset(csv2['XAcc_10m']),offset(csv2['YAcc_10m']),offset(csv2['ZAcc_10m'])]
				elif output_format == 'Disp':
					df_data3 = [offset(csv2['XDisp_20m']),offset(csv2['YDisp_20m']),offset(csv2['ZDisp_20m'])]
					df_data4 = [offset(csv2['XDisp_10m']),offset(csv2['YDisp_10m']),offset(csv2['ZDisp_10m'])]
				elif output_format == 'Ang':
					df_data3 = [convertanglelist(csv2['trackerAngle_20m'])]
					df_data4 = [convertanglelist(csv2['trackerAngle_10m'])]

				xdates2 = []

				for j in csv2['TIMESTAMP']:
					try:
						xdates2.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f"))
					except:
						xdates2.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S"))
				x = md.date2num(xdates2)
				axes[1,0].xaxis.set_major_formatter(xfmt)
				if output_format == 'Ang':
					axes[1,0].plot(x,df_data3[0],x,df_data4[0])
				else:
					axes[1,0].plot(x, df_data3[0],x,df_data3[1],x,df_data3[2],alpha=0.4)
				axes[1,0].set_ylabel(output_format_label)
				axes[1,0].set_ylim(axislim[0],axislim[1])
				axes[1,0].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')

				df_disp_twin3 = axes[1,0].twinx()
				df_disp_twin3.xaxis.set_major_formatter(xfmt)
				df_disp_twin3.set_ylabel('Wind [mph]')
				df_disp_twin3.set_ylim(windlim[0],windlim[1])
				df_disp_twin3.plot(xdates2,df_wind2,color='m')

				if output_format == 'Acc':
					axes[1,0].legend(['XAcc_20m','YAcc_20m','ZAcc_20m'])
				elif output_format == 'Disp':
					axes[1,0].legend(['XDisp_20m','YDisp_20m','ZDisp_20m'])
				elif output_format == 'Ang':
					axes[1,0].legend(['trackerAngle_20m','trackerAngle_10m'])

				if output_format == 'Ang':
					pass
				else:
					axes[1,1].xaxis.set_major_formatter(xfmt)
					axes[1,1].plot(x, df_data4[0],x,df_data4[1],x,df_data4[2],alpha=0.4)
					axes[1,1].set_ylabel(output_format_label)
					axes[1,1].set_ylim(axislim[0],axislim[1])
					axes[1,1].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
					df_disp_twin4 = axes[1,1].twinx()
					df_disp_twin4.xaxis.set_major_formatter(xfmt)
					df_disp_twin4.set_ylabel('Wind [mph]')
					df_disp_twin4.set_ylim(windlim[0],windlim[1])
					df_disp_twin4.plot(xdates2,df_wind2,color='m')
					if output_format == 'Acc':
						axes[1,1].legend(['XAcc_10m','YAcc_10m','ZAcc_10m'])
					elif output_format == 'Disp':
						axes[1,1].legend(['XDisp_10m','YDisp_10m','ZDisp_10m'])

				try:
					only1697.pop(only1697.index(filename_second))
				except:
					pass
			except:
				pass

			# Save figure
			fig.savefig(savepath + '\\' + filename[:-4] + '_' + output_format + '.jpg')
			plt.close()

			# run myAnimate.py if requested
			if animateYN == 'Y':
				myAnimate(i)
				animations_made += 2
				print 'ANIMATION DONE'
			else:
				pass
			images_made += 1

	#generates secondary graph only if not plotted during primary loop
	for i in only1697:
		filename = i
		filedate = i[14:24]
		savepath = exportpath + '\\' + filedate + '\\' + output_format 
		if not os.path.exists(savepath):
			print 'CREATING DIRECTORY ' + savepath
			os.makedirs(savepath)
		else:
			pass
		existfiles = [a for a in listdir(savepath) if isfile(join(savepath,a))]
		if filename[:-4] + '_' + output_format + '.jpg' in existfiles and overwriteYN == 'N':
			pass
		else:
			csv = pandas.read_csv(datapath + '\\' +  filename,header = 1,skiprows = [2,3,4,5])
			
			if len(csv['TIMESTAMP'])<5:
				continue
			
			# Create and configure subplots
			fig,axes = plt.subplots(nrows=2,ncols=3)
			fig.set_size_inches(25,15)
			plt.tight_layout(pad=7, w_pad=7, h_pad=6)
			
			if output_format == 'Acc':
				axislim = [-.2,.2]
			elif output_format == 'Disp':
				axislim = [-2,2]
			elif output_format == 'Ang':
				axislim = [-35,35]

			windlim = [0,40]
			xfmt = md.DateFormatter('%H:%M:%S')

			# Configure xy data
			df_wind = csv[['wind_sp']]
			xdates = []

			for j in csv['TIMESTAMP']:
				try:
					xdates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f"))
				except:
					xdates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S"))

			x = md.date2num(xdates)

			if output_format == 'Acc':
				df_data = [offset(csv['XAcc_20m']),offset(csv['YAcc_20m']),offset(csv['ZAcc_20m'])]
				df_data1 = [offset(csv['XAcc_10m']),offset(csv['YAcc_10m']),offset(csv['ZAcc_10m'])]

			elif output_format == 'Disp':
				df_data = [offset(csv['XDisp_20m']),offset(csv['YDisp_20m']),offset(csv['ZDisp_20m'])]
				df_data1 = [offset(csv['XDisp_10m']),offset(csv['YDisp_10m']),offset(csv['ZDisp_10m'])]
			elif output_format == 'Ang':
				df_data = [csv['trackerAngle_20m']+180]
				df_data1 = [csv['trackerAngle_10m']+180]
			# Plot primary acc or disp data 50m
			axes[0,0].xaxis.set_major_formatter(xfmt)
			if output_format == 'Ang':
				axes[0,0].plot(x,df_data[0],x,df_data1[0])
			else:
				axes[0,0].plot(x, df_data[0],x,df_data[1],x,df_data[2],alpha=0.4)
			axes[0,0].set_ylabel(output_format_label)
			axes[0,0].set_ylim(axislim[0],axislim[1])
			axes[0,0].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
			axes[0,0].set_title(filename)
			# Plot twin wind data over same plot
			df_disp_twin = axes[0,0].twinx()
			df_disp_twin.xaxis.set_major_formatter(xfmt)
			df_disp_twin.set_ylabel('Wind [mph]')
			df_disp_twin.set_ylim(windlim[0],windlim[1])
			df_disp_twin.plot(x,df_wind,color='m')
			# Change legend based on desired output_format
			if output_format == 'Acc':
				axes[0,0].legend(['XAcc_20m','YAcc_20m','ZAcc_20m'])
			elif output_format == 'Disp':
				axes[0,0].legend(['XDisp_20m','YDisp_20m','ZDisp_20m'])
			elif output_format == 'Ang':
				axes[0,0].legend(['trackerAngle_20m','trackerAngle_10m'])

			if output_format == 'Ang':
				pass
			else:
				# Plot primary acc or disp data 40m
				axes[0,1].xaxis.set_major_formatter(xfmt)
				axes[0,1].plot(x, df_data1[0],x,df_data1[1],x,df_data1[2],alpha=0.4)
				axes[0,1].set_ylabel(output_format_label)
				axes[0,1].set_ylim(axislim[0],axislim[1])
				axes[0,1].set_xticklabels(csv['TIMESTAMP'],rotation='vertical')
				# Plot twin wind data over same plot
				df_disp_twin1 = axes[0,1].twinx()
				df_disp_twin1.xaxis.set_major_formatter(xfmt)
				df_disp_twin1.set_ylabel('Wind [mph]')
				df_disp_twin1.set_ylim(windlim[0],windlim[1])
				df_disp_twin1.plot(x,df_wind,color='m')
				# Change legend based on desired output_format
				if output_format == 'Acc':
					axes[0,1].legend(['XAcc_10m','YAcc_10m','ZAcc_10m'])
				elif output_format == 'Disp':
					axes[0,1].legend(['XDisp_10m','YDisp_10m','ZDisp_10m'])

			# Save figure
			fig.savefig(savepath + '\\' + filename[:-4] + '_' + output_format + '.jpg')
			plt.close()

			# run myAnimate.py if requested
			if animateYN == 'Y':
				myAnimate(i)
				animations_made += 2
				print 'ANIMATION DONE'
			else:
				pass
			images_made += 1

	print 'DONE! ' + str(images_made) + ' images created, and ' + str(animations_made) + ' animations.'

if __name__ == "__main__":
	main(get_inputs())
else:
	inputs = write_inputs()
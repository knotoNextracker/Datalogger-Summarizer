def myAnimate(filename):
	import os
	import numpy
	import pandas
	import numpy
	import matplotlib.pyplot as plt
	import time
	import matplotlib.animation as animation
	import math
	import matplotlib.dates as md
	import datetime as dt

	mypath = "C:\Users\knotohamiprodjo\Desktop\py_data\NEW"
	exportpath = "C:\Users\knotohamiprodjo\Desktop\py_dev"
	
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
	# Ensure .dat format
	if '.dat' in filename:
		nodat_filename = filename[:-4]
		pass
	else:
		nodat_filename = filename
		filename += '.dat'

	# Primary datalogger animate code
	if not '1696' in filename:
		print 'NOT PRIMARY DATALOGGER'
	else:
		csv = pandas.read_csv(mypath + '\\' +  str(filename), header = 1, skiprows = [2,3,4,5]) #creates data frame
		#try to grab secondary logger data
		try:
			filename_second = filename[0:7] + '7' + filename[8:]
			csv2 = pandas.read_csv(mypath + '\\' +  str(filename_second), header = 1, skiprows = [2,3,4,5]) #creates data frame
			secondary_available = True
		except:
			secondary_available = False
		# plotting initialization
		axes = [[],[],[]]
		fig = plt.figure()
		fig.set_size_inches(15,15)
		for i in range(0,3):
			axes[0].append(plt.subplot2grid((3,3),(0,i),colspan=1))
		plt.tight_layout(pad=7, w_pad=2, h_pad=6)
		# plotting parameters
		scaleby = 4
		dim = 2
		for i in range(0,3):
			axes[0][i].set_aspect('equal')
			axes[0][i].set_xlim(-dim,dim)
			axes[0][i].set_ylim(-dim,dim)
			axes[0][i].grid(which='both')
			axes[0][i].set_xlabel('Displacement [cm]')
			axes[0][i].set_ylabel('Displacement [cm]')
		#create points and line instances for first row IF POSSIBLE
		pt20m, = axes[0][0].plot([],[],'ro',zorder = 10)
		pt10m, = axes[0][0].plot([],[],'bo',zorder = 10)
		line20m, = axes[0][0].plot([],[],'r-',zorder = 1,alpha = .5)
		line10m, = axes[0][0].plot([],[],'b-',zorder = 1,alpha = .5)
		axes[0][0].legend(['20m','10m'])
		#create points and line instances for second row
		pt40m, = axes[0][1].plot([],[],'ro',zorder = 10)
		pt30m, = axes[0][1].plot([],[],'bo',zorder = 10)
		line40m, = axes[0][1].plot([],[],'r-',zorder = 1,alpha = .5)
		line30m, = axes[0][1].plot([],[],'b-',zorder = 1,alpha = .5)
		axes[0][1].legend(['40m','30m'])
		#create points and line instances for inner row
		pt50m, = axes[0][2].plot([],[],'ro',zorder = 10)
		line50m, = axes[0][2].plot([],[],'r-',zorder = 1,alpha = .5)
		axes[0][2].legend(['50m'])
		#initalize historic data lists
		linedata_50m, linedata_40m, linedata_30m, linedata_20m, linedata_10m = [],[],[],[],[]
		ptdata_50m, ptdata_40m, ptdata_30m, ptdata_20m, ptdata_10m = [],[],[],[],[]
		x_50m, x_40m, x_30m, x_20m, x_10m = [],[],[],[],[]
		y_50m, y_40m, y_30m, y_20m, y_10m = [],[],[],[],[]
		#create displacement historic data list and point data
		for i in range(0,len(csv['YDisp_40m'])):
			if i%scaleby == 0:
				x_50m.append(csv['YDisp_50m'][i])
				y_50m.append(csv['ZDisp_50m'][i])
				x_40m.append(csv['YDisp_40m'][i])
				y_40m.append(csv['ZDisp_40m'][i])
				x_30m.append(csv['YDisp_30m'][i])
				y_30m.append(csv['ZDisp_30m'][i])
				ptdata_50m.append([x_50m[-1],y_50m[-1]])
				ptdata_40m.append([x_40m[-1],y_40m[-1]])
				ptdata_30m.append([x_30m[-1],y_30m[-1]])
				if secondary_available:
					try:
						x_20m.append(csv2['YDisp_20m'][i])
						y_20m.append(csv2['ZDisp_20m'][i])
						x_10m.append(csv2['YDisp_10m'][i])
						y_10m.append(csv2['ZDisp_10m'][i])
						ptdata_20m.append([x_20m[-1],y_20m[-1]])
						ptdata_10m.append([x_10m[-1],y_10m[-1]])
					except:
						x_20m.append(0)
						y_20m.append(0)
						x_10m.append(0)
						y_10m.append(0)
						ptdata_20m.append([x_20m[-1],y_20m[-1]])
						ptdata_10m.append([x_10m[-1],y_10m[-1]])
		#concatenate historic data into x,y list
		linedata_50m = [x_50m,y_50m]
		linedata_40m = [x_40m,y_40m]
		linedata_30m = [x_30m,y_30m]

		npts = int(len(ptdata_40m)) #create number of frames using scaleby

		#create secondary linedata lists if possible
		if secondary_available:
			linedata_20m = [x_20m,y_20m]
			linedata_10m = [x_10m,y_10m]
		else:
			linedata_20m = [[0]*npts,[0]*npts]
			linedata_10m = [[0]*npts,[0]*npts]
		

		#angle animation
		#create three subplots in row 2 for angle
		for i in range(0,3):
			axes[1].append(plt.subplot2grid((3,3),(1,i),colspan=1))
		#graph parameters
		angledim = 2
		angle_titles = ['row 1 angle','row 2 angle','row 4 angle']
		angle_legends = [['20m','10,'],['40m','30m'],['50m']]
		#initialize graphs
		for i in range(0,3):
			axes[1][i].set_aspect('equal')
			axes[1][i].set_xlim(-angledim,angledim)
			axes[1][i].set_ylim(-angledim,angledim)
			axes[1][i].grid(which='both')
			axes[1][i].set_title(angle_titles[i])

		#create plots for tracker angle representation
		lineangle2_50m, = axes[1][2].plot([],[],'r-')
		lineangle2_40m, = axes[1][1].plot([],[],'r-')
		lineangle2_30m, = axes[1][1].plot([],[],'b-')
		lineangle2_20m, = axes[1][0].plot([],[],'r-')
		lineangle2_10m, = axes[1][0].plot([],[],'b-')

		# #create plots for tracker angle histogram
		# ax_lineangle_50m = axes[1][2].twinx()
		# ax_lineangle_40m = axes[1][1].twinx()
		# ax_lineangle_30m = axes[1][1].twinx()
		# ax_lineangle_20m = axes[1][0].twinx()
		# ax_lineangle_10m = axes[1][0].twinx()
		# twin_axes = [ax_lineangle_50m,ax_lineangle_40m,ax_lineangle_30m,ax_lineangle_20m,ax_lineangle_10m]
		# for i in twin_axes:
		# 	i.set_ylabel('Tracker Angle [deg]')
		# 	i.set_ylim(-180,180)
		# 	i.set_aspect('equal')
		# lineangle_50m, = ax_lineangle_50m.plot([],[],'r-')
		# lineangle_40m, = ax_lineangle_40m.plot([],[],'r-')
		# lineangle_30m, = ax_lineangle_30m.plot([],[],'b-')
		# lineangle_20m, = ax_lineangle_20m.plot([],[],'r-')
		# lineangle_10m, = ax_lineangle_10m.plot([],[],'b-')

		#assign legends to plots
		axes[1][0].legend(['20m','10m'])
		axes[1][1].legend(['40m','30m'])
		axes[1][2].legend(['50m'])
		#initialize angle data lists
		linedata_angle50m, linedata_angle40m, linedata_angle30m, linedata_angle20m, linedata_angle10m = [],[],[],[],[]
		#do math and create line points for angles
		angle_50m, angle_40m, angle_30m, angle_20m, angle_10m = [],[],[],[],[]
		degangle_50m, degangle_40m, degangle_30m, degangle_20m, degangle_10m = [],[],[],[],[]
		for i in range(0,len(csv['trackerAngle_40m'])):
			if i%scaleby == 0:
				degangle_50m.append(totrackerangle(csv['trackerAngle_40m'][i]))
				degangle_40m.append(csv['trackerAngle_40m'][i]+180)
				degangle_30m.append(csv['trackerAngle_30m'][i]+180)
				angle_50m.append(math.radians(totrackerangle(csv['trackerAngle_40m'][i])))
				angle_40m.append(math.radians(totrackerangle(csv['trackerAngle_40m'][i])))
				angle_30m.append(math.radians(totrackerangle(csv['trackerAngle_30m'][i])))
				if secondary_available:
					try:
						angle_20m.append(math.radians(totrackerangle(csv2['trackerAngle_20m'][i])))
						angle_10m.append(math.radians(totrackerangle(csv2['trackerAngle_10m'][i])))
						# degangle_20m.append(totrackerangle(csv['trackerAngle_20m'][i]))
						# degangle_10m.append(totrackerangle(csv['trackerAngle_10m'][i]))
					except:
						print 'SECONDARY ANGLE FAILED'
						angle_20m.append(0)
						angle_10m.append(0)
				else:
					angle_20m.append(0)
					angle_10m.append(0)
				x_50mangle = [math.cos(angle_50m[-1]), -math.cos(angle_50m[-1])]
				y_50mangle = [math.sin(angle_50m[-1]), -math.sin(angle_50m[-1])]
				x_40mangle = [math.cos(angle_40m[-1]), -math.cos(angle_40m[-1])]
				y_40mangle = [math.sin(angle_40m[-1]), -math.sin(angle_40m[-1])]
				x_30mangle = [math.cos(angle_30m[-1]), -math.cos(angle_30m[-1])]
				y_30mangle = [math.sin(angle_30m[-1]), -math.sin(angle_30m[-1])]
				x_20mangle = [math.cos(angle_20m[-1]), -math.cos(angle_20m[-1])]
				y_20mangle = [math.sin(angle_20m[-1]), -math.sin(angle_20m[-1])]
				x_10mangle = [math.cos(angle_10m[-1]), -math.cos(angle_10m[-1])]
				y_10mangle = [math.sin(angle_10m[-1]), -math.sin(angle_10m[-1])]
				linedata_angle50m.append([x_50mangle, y_50mangle])
				linedata_angle40m.append([x_40mangle, y_40mangle])
				linedata_angle30m.append([x_30mangle, y_30mangle])
				linedata_angle20m.append([x_20mangle, y_20mangle])
				linedata_angle10m.append([x_10mangle, y_10mangle])
		# x1 = numpy.linspace(-angledim, angledim, len(degangle_50m))
		# x2 = numpy.linspace(-angledim, angledim, len(degangle_20m))
		#windspeed animation
		xfmt = md.DateFormatter('%H:%M:%S')
		windlim = [0,40] #y limits
		axes[2].append(plt.subplot2grid((3,3),(2,0),colspan=3)) #create 3-wide subplot in row 3
		#initialize plot and lines
		axes[2][0].set_ylim(windlim[0],windlim[1])
		axes[2][0].grid(which='both')
		linewind, = axes[2][0].plot([],[],'k-')
		ptwind, = axes[2][0].plot([],[],'ro')
		axes[2][0].legend(['Windspeed'])
		windvalues = []
		winddata = []

		timedates = []

		for j in csv['TIMESTAMP']:
			if len(j) > 19:
				timedates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f"))
			else:
				timedates.append(md.datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S"))

		timenum = md.date2num(timedates)
		timedata = []
		timelabels = []
		for i in range(0,len(csv['trackerAngle_40m'])):
			if i%scaleby == 0:
				timedata.append(timenum[i])
				windvalues.append(csv['wind_sp'][i])
				timelabels.append(csv['TIMESTAMP'][i])
		winddata = [timedata,windvalues]
		axes[2][0].set_xlim(min(timedata),max(timedata))
		axes[2][0].set_xlabel('Time')
		axes[2][0].set_ylabel('Windspeed [mph]')
		axes[2][0].xaxis.set_major_formatter(xfmt)
		axes[2][0].set_title('Windspeed over time')

		#animation intialization and animation
		def init():
			line50m.set_data([],[])
			pt50m.set_data([],[])
			line40m.set_data([],[])
			pt30m.set_data([],[])
			line30m.set_data([],[])
			pt20m.set_data([],[])
			line20m.set_data([],[])
			pt10m.set_data([],[])
			line10m.set_data([],[])

			lineangle2_50m.set_data([],[])
			lineangle2_40m.set_data([],[])
			lineangle2_30m.set_data([],[])
			lineangle2_20m.set_data([],[])
			lineangle2_10m.set_data([],[])

			# lineangle_50m.set_data([],[])
			# lineangle_40m.set_data([],[])
			# lineangle_30m.set_data([],[])
			# lineangle_20m.set_data([],[])
			# lineangle_10m.set_data([],[])

			linewind.set_data([],[])
			ptwind.set_data([],[])

			return pt40m,

		def animate(i):
			axes[0][1].set_title(nodat_filename[0:14] + csv['TIMESTAMP'][i*scaleby][0:19])
			line50m.set_data(linedata_50m[0][:i],linedata_50m[1][:i])
			pt50m.set_data(ptdata_50m[i][0], ptdata_50m[i][1])
			line40m.set_data(linedata_40m[0][:i],linedata_40m[1][:i])
			pt40m.set_data(ptdata_40m[i][0], ptdata_40m[i][1])
			line30m.set_data(linedata_30m[0][:i],linedata_30m[1][:i])
			pt30m.set_data(ptdata_30m[i][0], ptdata_30m[i][1])
			line20m.set_data(linedata_20m[0][:i],linedata_20m[1][:i])
			pt20m.set_data(ptdata_20m[i][0], ptdata_20m[i][1])
			line10m.set_data(linedata_10m[0][:i],linedata_10m[1][:i])
			pt10m.set_data(ptdata_10m[i][0], ptdata_10m[i][1])

			lineangle2_50m.set_data(linedata_angle50m[i][0],linedata_angle50m[i][1])
			lineangle2_40m.set_data(linedata_angle40m[i][0],linedata_angle40m[i][1])
			lineangle2_30m.set_data(linedata_angle30m[i][0],linedata_angle30m[i][1])
			lineangle2_20m.set_data(linedata_angle20m[i][0],linedata_angle20m[i][1])
			lineangle2_10m.set_data(linedata_angle10m[i][0],linedata_angle10m[i][1])

			# lineangle_50m.set_data(x1,degangle_50m)
			# lineangle_40m.set_data(x1,degangle_40m)
			# lineangle_30m.set_data(x1,degangle_30m)
			# lineangle_20m.set_data(x2,degangle_20m)
			# lineangle_10m.set_data(x2,degangle_10m)

			linewind.set_data(winddata[0],winddata[1])
			ptwind.set_data(winddata[0][i],winddata[1][i])
			for tick in axes[2][0].xaxis.iter_ticks():
				tick[0].label1.set_rotation('vertical')
			fig.canvas.draw()
			return pt40m,

		myfps = 50/scaleby
		anim = animation.FuncAnimation(fig, animate, init_func = init, frames=npts, interval=myfps, blit=False)
		# plt.show() #uncomment to show plot during execution
		# write as mp4
		Writer = animation.writers['ffmpeg']
		writer = Writer(fps=myfps,bitrate=1800)
		start_time = time.time()
		print 'Start Time: ' + dt.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
		print 'Creating video @ ' + str(myfps) + ' fps and ' + str(npts) + ' total frames.....'
		print 'Estimated time to complete: ' + str(npts*.79/60) + ' minutes.'
		anim.save(exportpath + "\VIDEOS\\" + nodat_filename + ".mp4",writer=writer) #uncomment to save plot
		elapsed_time = time.time() - start_time
		print 'COMPLETE. Total Time: ' + str(elapsed_time/60) + ' minutes.'
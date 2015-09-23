import numpy
import pandas
import logging
import matplotlib.dates as md
import time
import datetime


def main(filename):
    logger = logging.getLogger("Summarizer_Loop")
    mypath = "\\\\10.10.1.150\das\Garnet"
    csv = pandas.read_csv(mypath + '\\' +  filename, header = 1, skiprows = [2,3,4,5]) #creates data frame

    def magnitude(a,b,c):
        return numpy.sqrt(numpy.add(numpy.add(numpy.square(a),numpy.square(b)),numpy.square(c)))
    def totrackerangle(angle):
        if angle > 0:
            return  - (180 - angle)
        else:
            return  - (- 180 - angle)
    
    wind_sp = csv['wind_sp']

    try:
        XAcc_30m = csv['XAcc_30m']
        YAcc_30m = csv['YAcc_30m']
        ZAcc_30m = csv['ZAcc_30m']
        if len(XAcc_30m)<5:
            logger.debug(filename + " is too short! Skipping...")
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            pass
        magAcc_30m = magnitude(XAcc_30m,YAcc_30m,ZAcc_30m)
        XAcc_40m = csv['XAcc_40m']
        YAcc_40m = csv['YAcc_40m']
        ZAcc_40m = csv['ZAcc_40m']
        magAcc_40m = magnitude(XAcc_40m,YAcc_40m,ZAcc_40m)
        XAcc_50m = csv['XAcc_50m']
        YAcc_50m = csv['YAcc_50m']
        ZAcc_50m = csv['ZAcc_50m']
        magAcc_50m = magnitude(XAcc_50m,YAcc_50m,ZAcc_50m)
        maxAccel_mag = max(max(magAcc_30m),max(magAcc_40m),max(magAcc_50m))

        XDisp_30m = csv['XDisp_30m']
        YDisp_30m = csv['YDisp_30m']
        ZDisp_30m = csv['ZDisp_30m']
        magDisp_30m = magnitude(XDisp_30m,YDisp_30m,ZDisp_30m)
        XDisp_40m = csv['XDisp_40m']
        YDisp_40m = csv['YDisp_40m']
        ZDisp_40m = csv['ZDisp_40m']
        magDisp_40m = magnitude(XDisp_40m,YDisp_40m,ZDisp_40m)
        XDisp_50m = csv['XDisp_50m']
        YDisp_50m = csv['YDisp_50m']
        ZDisp_50m = csv['ZDisp_50m']
        magDisp_50m = magnitude(XDisp_50m,YDisp_50m,ZDisp_50m)
        maxDisp_mag = max(max(magDisp_30m),max(magDisp_40m),max(magDisp_50m))
        angle_names = ['trackerAngle_50m','trackerAngle_40m','trackerAngle_30m']
        for name in angle_names:
            out = []
            for a in csv[name]:
                out.append(totrackerangle(a))
            csv[name] = out
        avgAngle30m = numpy.average(csv['trackerAngle_30m'])
        avgAngle40m = numpy.average(csv['trackerAngle_40m'])
        avgAngle50m = numpy.average(csv['trackerAngle_50m'])
        avgTrackerAngle = numpy.average([avgAngle30m, avgAngle40m])

    except:
        XAcc_20m = csv['XAcc_20m']
        YAcc_20m = csv['YAcc_20m']
        ZAcc_20m = csv['ZAcc_20m']
        if len(XAcc_20m)<5:
            logger.debug(filename + " is too short! Skipping...")
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            pass
        magAcc_20m = magnitude(XAcc_20m,YAcc_20m,ZAcc_20m)
        XAcc_10m = csv['XAcc_10m']
        YAcc_10m = csv['YAcc_10m']
        ZAcc_10m = csv['ZAcc_10m']
        magAcc_10m = magnitude(XAcc_10m,YAcc_10m,ZAcc_10m)
        maxAccel_mag = max(max(magAcc_20m),max(magAcc_10m))

        XDisp_20m = csv['XDisp_20m']
        YDisp_20m = csv['YDisp_20m']
        ZDisp_20m = csv['ZDisp_20m']
        magDisp_20m = magnitude(XDisp_20m,YDisp_20m,ZDisp_20m)
        XDisp_10m = csv['XDisp_10m']
        YDisp_10m = csv['YDisp_10m']
        ZDisp_10m = csv['ZDisp_10m']
        magDisp_10m = magnitude(XDisp_10m,YDisp_10m,ZDisp_10m)
        maxDisp_mag = max(max(magDisp_10m),max(magDisp_20m))

        angle_names = ['trackerAngle_20m','trackerAngle_10m']
        for name in angle_names:
            out = []
            for a in csv[name]:
                out.append(totrackerangle(a))
            csv[name] = out
        avgAngle20m = numpy.average(csv['trackerAngle_20m'])
        avgAngle10m = numpy.average(csv['trackerAngle_10m'])
        avgTrackerAngle = numpy.average([avgAngle20m, avgAngle10m])
    try:
        timestart = md.datetime.datetime.strptime(csv['TIMESTAMP'][len(csv['TIMESTAMP'])-1], "%Y-%m-%d %H:%M:%S.%f")
    except:
        timestart = md.datetime.datetime.strptime(csv['TIMESTAMP'][len(csv['TIMESTAMP'])-1], "%Y-%m-%d %H:%M:%S")
    try:
        timeend = md.datetime.datetime.strptime(csv['TIMESTAMP'][0], "%Y-%m-%d %H:%M:%S.%f") 
    except:
        timeend = md.datetime.datetime.strptime(csv['TIMESTAMP'][0], "%Y-%m-%d %H:%M:%S") 
    time_delta = timestart - timeend

    dt = datetime.datetime
    times = []
    for idx,i in csv['TIMESTAMP'].iteritems():
        try:
            times.append(dt.strptime(i, "%Y-%m-%d %H:%M:%S.%f"))
        except:
            times.append(dt.strptime(i, "%Y-%m-%d %H:%M:%S"))

    for idx,val in enumerate(times):
        if idx == 0:
            pass
        else:
            if val - times[idx-1] > datetime.timedelta(seconds = 15):
                first_event_end = dt.strftime(val,"%Y-%m-%d %H:%M:%S")
                break
        first_event_end = dt.strftime(val,"%Y-%m-%d %H:%M:%S")

    return [csv['TIMESTAMP'].iloc[0][0:19],csv['TIMESTAMP'].iloc[-1][0:19],csv['TIMESTAMP'].iloc[0][11:16],max(wind_sp), maxAccel_mag, maxDisp_mag, avgTrackerAngle,time_delta.total_seconds(),time_delta.total_seconds()/len(csv['TIMESTAMP']),first_event_end]
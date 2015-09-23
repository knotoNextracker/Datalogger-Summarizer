import Summarizer
import time
import logging
logging.getLogger(__name__)
logging.basicConfig(filename='Summarizer_loop.log',level=logging.DEBUG,format ='%(asctime)s %(message)s')
logging.info("Begin execution " + str(time.strftime("%a, %d %b %Y %H:%M:%S")))
while True:
	logging.info("Excecuting Summarizer at %r" % time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
	print "Excecuting Summarizer at %r" % time.strftime("%m/%d/%y %H:%M:%S",time.localtime())
	Summarizer.main()
	sleeptime = 30
	logging.info("Waiting for %r minutes before next execution." % sleeptime)
	print "Waiting for %r minutes before next execution." % sleeptime
	logging.info("Start wait: %r" % time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
	with open('Summarizer_Loop Execution Log.txt','a') as log_file:
		log_file.write('Execution completed at %r' % time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
		log_file.write('\n')
	print "Start wait: %r" % time.strftime("%m/%d/%y %H:%M:%S",time.localtime())
	time.sleep(sleeptime*60)
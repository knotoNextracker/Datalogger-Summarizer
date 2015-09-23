import Summarizer
import time
import logging

logging.basicConfig(level=logging.DEBUG,format ='%(asctime)s [%(module)s]: %(message)s')
logger = logging.getLogger("Summarizer_Loop")
debug_log = logging.FileHandler('Summarizer_Loop Debug.log')
debug_log.setLevel(logging.DEBUG)
debug_log.setFormatter(logging.Formatter('%(asctime)s [%(module)s]: %(message)s'))
info_log = logging.FileHandler('Summarizer_Loop Info.log')
info_log.setLevel(logging.INFO)
info_log.setFormatter(logging.Formatter('%(asctime)s [%(module)s]: %(message)s'))

logger.addHandler(debug_log)
logger.addHandler(info_log)

logger.info("---------- Begin Summarizer_Loop execution ----------")
while True:
	logger.info("----- Excecuting Summarizer -----")
	Summarizer.main()
	with open('Summarizer_Loop Execution Log.txt','a') as log_file:
		log_file.write('Execution completed at %r' % time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
		log_file.write('\n')
	sleeptime = 30
	logger.info("Waiting for %r minutes before next execution." % sleeptime)
	logger.info("Start wait...")
	time.sleep(sleeptime*60)
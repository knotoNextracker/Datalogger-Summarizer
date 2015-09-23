import Summarizer
import time
import logging
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')
module_name = 'Summarizer_Loop'
logger_format = '%(asctime)s [%(module)s]: %(message)s'
logging.basicConfig(level=logging.DEBUG,format = logger_format)
logger = logging.getLogger(config.get('Logger','logger_name'))
debug_log = logging.FileHandler('Summarizer_Loop Debug.log')
debug_log.setLevel(logging.DEBUG)
debug_log.setFormatter(logging.Formatter(logger_format))
info_log = logging.FileHandler('Summarizer_Loop Info.log')
info_log.setLevel(logging.INFO)
info_log.setFormatter(logging.Formatter(logger_format))

logger.addHandler(debug_log)
logger.addHandler(info_log)

logger.info("---------- Begin Summarizer_Loop execution ----------")

while True:
	logger.info("----- Excecuting Summarizer -----")
	Summarizer.main()
	with open('Summarizer_Loop Execution Log.txt','a') as log_file:
		log_file.write('Execution completed at %r' % time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
		log_file.write('\n')
	sleeptime = config.getfloat(module_name, 'wait_time')
	logger.info("Waiting for %r minutes before next execution." % sleeptime)
	logger.info("Start wait...")
	time.sleep(sleeptime*60)
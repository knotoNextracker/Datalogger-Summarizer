# Checks the Datalogger_Archive.xlsx spreadsheet agianst the check_filenames input. If a check_filenames 
# does not exist in the spreadsheet, it returns False. If return_list == True, it will output a list of all 
# the files missing from the spreadsheet.
import pandas
import logging

def main(check_filenames,return_list = False):
	# Try reading archive sheet, else return False
	logger = logging.getLogger("Summarizer_Loop")
	logger.info("----- Start Check_Archives ----")
	mypath = 'C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx'
	result = True
	try:
		excel = pandas.read_excel(mypath,sheetname = 'Sheet1')
	except:
		logger.debug("No archive!")
		if return_list == True:
			return []
		return False

	# Start comparing filenames and return the missing_files list
	missing_files = []
	for check_filename in check_filenames:
		if not check_filename in excel['Filename'].values:
			logger.debug(check_filename + ' NOT HERE')
			missing_files.append(check_filename)
			result = False
		else:
			continue
	if return_list == True:
		logger.debug("List of missing files: %r" % missing_files)
		return missing_files
	else:
		if len(missing_files) == 0:
			logger.debug("No files to update!")
		else:
			logger.debug("There are files to update!")
		return result
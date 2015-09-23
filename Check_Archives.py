# Checks the Datalogger_Archive.xlsx spreadsheet agianst the check_filenames input. If a check_filenames 
# does not exist in the spreadsheet, it returns False. If return_list == True, it will output a list of all 
# the files missing from the spreadsheet.
import pandas

def main(check_filenames,return_list = False):
	# Try reading archive sheet, else return False
	mypath = 'C:\Users\knotohamiprodjo\Desktop\py_dev\Datalogger_Archive.xlsx'
	result = True
	try:
		excel = pandas.read_excel(mypath,sheetname = 'Sheet1')
	except:
		return False

	# Start comparing filenames and return the missing_files list
	missing_files = []
	for check_filename in check_filenames:
		if not check_filename in excel['Filename'].values:
			print check_filename + ' NOT HERE'
			missing_files.append(check_filename)
			result = False
		else:
			continue
	if return_list == True:
		return missing_files
	else:
		return result
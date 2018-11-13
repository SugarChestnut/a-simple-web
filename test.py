try:
	with open('myfile.txt') as fh:
		file_data = fn.read()
	print (file_fata)
	
except FileNotFoundError:
	print('The data file is missing')
	
except PermissionError:
	print('This is not allowed')
	
except Exception as err:
	print('Some other error occurrde:', str(err))
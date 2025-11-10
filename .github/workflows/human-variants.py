import os
import re

def read_everything(data_folder):
	print('\nreading data folder')
	objs, obj_paths, obj_names = [], [], []
	started = False
	folders = os.listdir(data_folder)
	folders.append('')
	folders.sort()
	for folder in  folders:
		if os.path.isdir(data_folder + folder):
			text_files = os.listdir(data_folder + folder)
			text_files.sort()
			for text_file in text_files:
				if os.path.isfile(data_folder + folder + os.sep + text_file) == False:
					continue
				if len(folder + text_file)  < 80: # just for displaying / max len = 44(currently)
					count = 80 - len(folder + text_file)
					spaces = ''
					for i in range(0, count):
						spaces += ' '
				print('	reading: ' + folder + os.sep + text_file + spaces, end = '\r', flush= True)
				with open(data_folder + folder + os.sep + text_file, 'r') as source_file:
					lines = source_file.readlines()
				index = 0
				for line in lines:
					index += 1
					if line[:1] == '#':
						continue
					elif line == '\n':
						continue
					elif line == '\t\n':
						continue
					elif line == '\t\t\n':
						continue
					elif line[:1] != '\t' or index == len(lines):
						if started == True:
							objs.append(txt.replace('<', '&#60;').replace('>', '&#62;'))
							obj_paths.append(txt2)
							obj_names.append(txt3.replace('\t', ' '))
							started = False
						txt = line
						if folder != '':
							folder_fix = folder + os.sep
						else:
							folder_fix = folder
						txt2 = 'data' + os.sep + folder_fix + text_file
						txt3 = line[:len(line)-1]
						started = True
					else:
						if started == True:
							txt += line
	print('	\n	DONE')
	return objs, obj_paths, obj_names

def show_variants(objs):
	ships = []
	for obj in objs:
		if obj.startswith('ship '): # get all ships
			line = obj[:obj.find('\n')] # get just the first line i.e. ship "scrapper" "scrapper (gatling)"
			if '"' in line:
				pos1 = line.find('"')
				pos2 = line.find('"', pos1 +1)
				if obj[pos2 + 1] != '\n': # if a linebreak comes after the "scrapper"
					line = line.replace('ship ', '') # remove the 'ship ' before the name
					pos1 = line.find('"')
					pos2 = line.find('"', pos1 + 1)
					line = line[pos2 + 1:].strip() # only get the second token
					ships.append('\t' + line)
	with open('~/-Omnis/data/variants.txt', 'w') as target: # write to file
		for line in ships:
			target.writelines(line + '\n')
	print(str(len(ships)) + ' variants found')
	print('variants.txt written to: ' + os.getcwd())

if __name__ == "__main__":
	data_folder = "~/endless-sky/data/"
	objs, obj_paths, obj_names = read_everything(data_folder)
	show_variants(objs)

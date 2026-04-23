import os

def read_everything(data_folder):
	print('\nreading data folder')
	objs, obj_paths, obj_names = [], [], []
	started = False
	folders = os.listdir(data_folder)
	folders.append('')
	folders.sort()
	for folder in folders:
		if os.path.isdir(data_folder + folder):
			text_files = os.listdir(data_folder + folder)
			text_files.sort()
			for text_file in text_files:
				if os.path.isfile(data_folder + folder + os.sep + text_file) == False:
					continue
				if len(folder + text_file) < 80: # just for displaying / max len = 44(currently)
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


def filter_objs(obj_paths, obj_names, objs, ships_exclude, outfits_exclude):
	# variants check def, return True for variant, and False for ship
	variants_text = 'shipyard "variants"\n'
	def check_variants(nodename):
		if nodename.count('"') == 2:
			check = False
		else:
			check = True
		return check
	# filter all outfits and ships out of all nodes and save them with their paths
	print('filtering objects')
	ships, ships_path, outfits, outfits_path, variants, variants_path, variantsall, variantsall_path = [], [], [], [], [], [], [], []
	for obj_name in obj_names:
		index = obj_names.index(obj_name)
		path = obj_paths[index].split(os.sep)[1]
		path = path.replace('.txt', '')
		path = path.replace('persons', 'developer')
		path = path.replace('_deprecated', 'deprecated')
		if obj_name.startswith('ship '):
			if not obj_name.strip().replace('ship ', '').replace('"', '') in ships_exclude:
				check = check_variants(obj_name.strip())
				if check == False:
					ships.append(obj_name.strip().replace('ship ', ''))
					ships_path.append(path)
				else:
					line = obj_name
					if '"' in line:
						obj = objs[index]
						pos1 = line.find('"')
						pos2 = line.find('"', pos1 +1)
						if obj[pos2 + 1] != '\n': # if a linebreak comes after the "scrapper"
							line = line.replace('ship ', '') # remove the 'ship ' before the name
							pos1 = line.find('"')
							pos2 = line.find('"', pos1 + 1)
							name = line[pos2 + 1:].strip() # only get the second token
					if 'add attributes' in objs[index]:
						variants.append(name)
						variants_path.append(path)
					else:
						variantsall.append(name)
						variantsall_path.append(path)
		elif obj_name.startswith('outfit '):
			if not any(excluded_part in obj_name.strip().replace('outfit ', '').replace('"', '') for excluded_part in outfits_exclude):
				outfits.append(obj_name.strip().replace('outfit ', ''))
				outfits_path.append(path)
	print('		' + str(len(ships)) + ' ships found')
	print('		' + str(len(outfits)) + ' outfits found')
	return ships, ships_path, outfits, outfits_path, variants, variants_path, variantsall, variantsall_path


def create_shipyards(ships, ships_path, variants, variants_path, variantsall, variantsall_path):
	# create a text containing all shipyards and the matching ships
	listed_paths = []
	shipyards_text, variants_text, variantsall_text = '', '', ''
	for path in ships_path:
		if not path in listed_paths:
			listed_paths.append(path)
	print('		different shipyards found: ' + str(len(listed_paths)))
	#print(listed_paths)
	shipyards_text += 'shipyard "omnis"\n'
	shipyards_text += '	"Caster A"\n'
	shipyards_text += '	"Caster B"\n'
	shipyards_text += '	"Caster C"\n\n'
	for shipyard in listed_paths:
		shipyards_text += 'shipyard "' + shipyard + '"\n'
		if shipyard == "developer":
			shipyards_text += '	"Kestrel (MZ)"\n'
			shipyards_text += '	"Finch (MZ)"\n'
			shipyards_text += '	"Vanguard (Pointedstick)"\n'
			shipyards_text += '	"Subsidurial"\n'
		variants_text += 'shipyard "' + shipyard + 'Variants"\n'
		variantsall_text  += 'shipyard "' + shipyard + 'VariantsAll"\n'
		has_no_content = True
		for ship in ships:
			index = ships.index(ship)
			if ships_path[index] == shipyard:
				shipyards_text += '	' + ship + '\n'
				has_no_content = False
		if has_no_content == True:
			shipyards_text += '	"dummy"\n'
		shipyards_text += '\n'
		has_no_content = True
		for variant in variants:
			index = variants.index(variant)
			if variants_path[index] == shipyard:
				variants_text += '	' + variant + '\n'
				has_no_content = False
		if has_no_content == True:
			variants_text += '	"dummy"\n'
		variants_text += '\n'
		has_no_content = True
		for variantall in variantsall:
			index = variantsall.index(variantall)
			if variantsall_path[index] == shipyard:
				variantsall_text += '	' + variantall + '\n'
				has_no_content = False
		if has_no_content == True:
			variantsall_text += '	"dummy"\n'
		variantsall_text += '\n'
	return shipyards_text, variants_text, variantsall_text


def create_outfitter(outfits, outfits_path):
	# create a text containing all outfitter and the matching outfits
	listed_paths = []
	outfitter_text = ''
	for path in outfits_path:
		if not path in listed_paths:
			listed_paths.append(path)
	print('		different outfitters found: ' + str(len(listed_paths)))
	outfitter_text += 'outfitter "omnis"\n'
	outfitter_text += '	"   Omnipotence"\n'
	outfitter_text += '	"   Omnipresence"\n'
	outfitter_text += '	"   Omniscience"\n'
	outfitter_text += '	"  Disable"\n'
	outfitter_text += '	"  Kill"\n'
	outfitter_text += '	" Crux Stone "\n'
	outfitter_text += '	"Carry All"\n'
	outfitter_text += '	"Drag Addition"\n'
	outfitter_text += '	"Drag Reduction"\n'
	outfitter_text += '	"Extra Engine"\n'
	outfitter_text += '	"Extra Outfit"\n'
	outfitter_text += '	"Extra Weapon"\n'
	outfitter_text += '	"Fuel Capacity Addition"\n'
	outfitter_text += '	"Fuel Capacity Reduction"\n'
	outfitter_text += '	"Heat Dissipation Addition"\n'
	outfitter_text += '	"Heat Dissipation Reduction"\n'
	outfitter_text += '	"Mass Addition"\n'
	outfitter_text += '	"Mass Reduction"\n'
	outfitter_text += '	"Spinal Mount Addition"\n\n'
	has_no_content = True
	for outfitter in listed_paths:
		outfitter_text += 'outfitter "' + outfitter + '"\n'
		for outfit in outfits:
			index = outfits.index(outfit)
			if outfits_path[index] == outfitter:
				outfitter_text += '	' + outfit + '\n'
				has_no_content = False
		if has_no_content == True:
			outfitter_text += '	"dummy"\n'
		outfitter_text += '\n'
	return outfitter_text


def write_files(sales_file, shipyards_text, outfitter_text, variants_text, variantsall_text):
	# write text files
	merged_file = shipyards_text + '\n\n' + variants_text + '\n\n' + variantsall_text + outfitter_text
	with open(sales_file, 'w') as target:
		target.writelines(merged_file)


if __name__ == "__main__":
	data_folder = 'es-data/'
	sales_file = 'data/sales.txt'
	ships_exclude = ['Cloak Check', 'Asteroid Planet', 'Asteroid Blocker', '_Ion Timer Ship', 'Rescue Dummy', 'Timer Ship']
	outfits_exclude = ['Orchid Active', 'Orchid Boost', 'Orchid Coast', 'Orchid Divert', 'Orchid Terminal', 'Orchid Boost Stage Expended', 'Orchid Divert Stage Expended', 'Ophrys Terminal', 'ion hail', 'rslug', 'Blaster Submunition', 'Modified Blaster Submunition', 'gbullet', 'Suicide Gun', '_Ion Storm Timer: Generator', 'Timer Weapon', 'Timer Submunition', 'Shard inactive', 'static', 'print', 'asteroid fragment', 'magic deployer', 'asteroid missile', 'asteroid launch', 'ribault guided', 'ribault unguided', 'plasma particle', 'asteroid laser']
	objs, obj_paths, obj_names = read_everything(data_folder)
	ships, ships_path, outfits, outfits_path, variants, variants_path, variantsall, variantsall_path = filter_objs(obj_paths, obj_names, objs, ships_exclude, outfits_exclude)
	shipyards_text, variants_text, variantsall_text = create_shipyards(ships, ships_path, variants, variants_path, variantsall, variantsall_path)
	outfitter_text = create_outfitter(outfits, outfits_path)
	write_files(sales_file, shipyards_text, outfitter_text, variants_text, variantsall_text)

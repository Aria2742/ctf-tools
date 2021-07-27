def add_indents():
	orig = open('cpp.c', 'r')
	mod = open('cpp_mod.c', 'w')

	indent = 0
	S_level = 0
	for line in orig:
		temp_indent = 0
		if line.startswith('#if'):
			indent += 1
			temp_indent = -1
		elif line.startswith('#else'):
			temp_indent = -1
		elif line.startswith('#end'):
			indent -= 1
		for i in range(indent + temp_indent):
			mod.write('\t')
		mod.write(line)
		if line.startswith("#if S =="):
			for i in range(indent + temp_indent):
				mod.write('\t')
			mod.write(f'#warning S == {S_level}\n')
			S_level += 1

	orig.close()
	mod.close()

def clean_trace():
	orig = open('trace.txt', 'r')
	mod = open('trace_clean.txt', 'w')
	
	for line in orig:
		if line.startswith('cpp_mod.c'):
			mod.write(line)
	
	orig.close()
	mod.close()

"""
ROM = [187, 85, 171, 197, 185, 157, 201, 105, 187, 55, 217, 205, 33, 179, 207, 207, 159, 9, 181, 61, 235, 127, 87, 161, 235, 135, 103, 35, 23, 37, 209, 27, 8, 100, 100, 53, 145, 100, 231, 160, 6, 170, 221, 117, 23, 157, 109, 92, 94, 25, 253, 233, 12, 249, 180, 131, 134, 34, 66, 30, 87, 161, 40, 98, 250, 123, 27, 186, 30, 180, 179, 88, 198, 243, 140, 144, 59, 186, 25, 110, 206, 223, 241, 37, 141, 64, 128, 112, 224, 77, 28]
"""
def print_rom():
	orig = open('cpp.c', 'r')
	rom = [0 for x in range(0, 91)]
	
	for line in orig:
		if not line.startswith('#define ROM_0'):
			continue
		split_line = line.split('_')
		idx_str = split_line[1]
		idx = int(idx_str, 2)
		pow = split_line[2]
		pow = int(pow[0])
		bit_str = line[-2:-1]
		bit = int(bit_str)
		#print(f'{idx}, {pow}, {bit}')
		if bit == 1:
			rom[idx] += 1 << pow
	
	#for b in rom:
	#	print(f'{hex(b)}')
	print(f'Rom: {rom}')
	
	orig.close()

add_indents()
print_rom()
clean_trace()
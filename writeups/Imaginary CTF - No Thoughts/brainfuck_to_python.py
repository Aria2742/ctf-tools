source = open('flag_min.bf', 'r')

code = source.read()

source.close()

program_header = 'def print_mem():\n' + \
	'\tout = \'\'\n' + \
	'\tfor x in range(len(mem)):\n' + \
		'\t\tout += f\'{x:02x}\' + \' \'\n' + \
	'\tout += \'\\n\'\n' + \
	'\tout += \' \' * (ptr * 3)\n' + \
	'\tout += \'^\'\n' + \
	'\tprint(out)\n\n' + \
	'mem = [0 for x in range(1000)]\n' + \
	'ptr = 0\n' + \
	'input = \'test input\'\n' + \
	'input_idx = 0\n\n'

translated = program_header + ''
loops = 0
idx = 0

def repeats(code, char, idx):
	count = 0
	while code[idx] == char:
		count += 1
		idx += 1
	return count

def newline(pycode):
	return ('\t' * loops) + pycode + '\n'

while idx < len(code):
	if code[idx] == '[':
		translated += newline('while mem[ptr] != 0:')
		loops += 1
		idx += 1
	elif code[idx] == ']':
		loops -= 1
		idx += 1
	elif code[idx] == '>':
		delta = repeats(code, '>', idx)
		translated += newline(f'ptr += {delta}')
		idx += delta
	elif code[idx] == '<':
		delta = repeats(code, '<', idx)
		translated += newline(f'ptr -= {delta}')
		idx += delta
	elif code[idx] == '+':
		delta = repeats(code, '+', idx)
		translated += newline(f'mem[ptr] = (mem[ptr] + {delta}) & 0xFFFFFFFF')
		idx += delta
	elif code[idx] == '-':
		delta = repeats(code, '-', idx)
		translated += newline(f'mem[ptr] = (mem[ptr] - {delta}) & 0xFFFFFFFF')
		idx += delta
	elif code[idx] == ',':
		translated += newline('mem[ptr] = ord(input[input_idx])')
		translated += newline('input_idx += 1')
		idx += 1
	elif code[idx] == '.':
		translated += newline('print(chr(mem[ptr]))')
		idx += 1
	else:
		idx += 1

print(translated)
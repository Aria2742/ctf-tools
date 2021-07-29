import subprocess

build_cmd = 'iverilog -o abnormal_mod.vvp -s main abnormal_mod.v'.split(' ')
run_cmd = ['vvp', 'abnormal_mod.vvp']

orig = open('abnormal.v', 'r')
code = orig.read().split('\n')
orig.close()

flag = ['6','9','6','3','7','4','6','6','7','b','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0','0','0','0','0','0','7','d']
alpha = '0123456789abcdef'

for idx in range(len(flag)-1, -1, -1):
	for char in alpha:
		flag[idx] = char
		mod = open('abnormal_mod.v', 'w')
		for line in code:
			if line.startswith("    wire [255:0] flag = 256'h"):
				mod.write("    wire [255:0] flag = 256'h" + ''.join(flag) + ';\n)
			else:
				mod.write(line + '\n')
		mod.close()
		subprocess.run(build_cmd)
		out = subprocess.run(run_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
		
		if out[idx] == '0':
			break

print('Finished! Here\'s the flag:')
print(''.join(flag))

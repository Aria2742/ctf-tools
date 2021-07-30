import subprocess

# commands to cmpile and execute the Verilog file
build_cmd = 'iverilog -o abnormal_mod.vvp -s main abnormal_mod.v'.split(' ')
run_cmd = ['vvp', 'abnormal_mod.vvp']

# get the Verilog code to modify
orig = open('abnormal.v', 'r')
code = orig.read().split('\n')
orig.close()

flag = [x for x in '696374667b00000000000000000000000000000000000000000000000000007d']
alpha = '0123456789abcdef'

# go from right to left in the flag, brute forcing one hex char at a time
for idx in range(len(flag)-1, -1, -1):
    for char in alpha:
        flag[idx] = char
        # create a copy of the Verilog file with the modified flag
        mod = open('abnormal_mod.v', 'w')
        for line in code:
            if line.startswith("    wire [255:0] flag = 256'h"):
                mod.write("    wire [255:0] flag = 256'h" + ''.join(flag) + ';\n')
            else:
                mod.write(line + '\n')
        mod.close()
        # compile and run the Verilog file
        subprocess.run(build_cmd)
        out = subprocess.run(run_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        # did we guess the right (hex) char?
        if out[idx] == '0':
            print(''.join(flag))
            break

print('Finished! Here\'s the flag:')
print(''.join(flag))

# Abnormal

## Files
### Originals Provided w/ Challenge
 - [Makefile](./Makefile)
 - [abnormal.v](./abnormal.v)
### Created/Modified to Solve Challenge
 - [abnormal_edit.v](./abnormal_edit.v) - abnormal.v with added print statement used to brute-force the flag
 - [abnormal_brute.py](./abnormal_brute.py) - Python code to brute-force the flag one character at a time

## Description
For this challenges, we're provided with Verilog source code. The previous challenge, "Normal", included a makefile with the commands to compile and run the source code. The commands to compile and run the Verilog file are as follows:

compile: `iverilog -o normal.vvp -s main normal.v`  
run: `vvp normal.vvp`

## Initial Analysis
The code consists of 5 different modules (which act like functions):
  - main
  - abnormal
  - norc
  - narb
  - nora

### Main & Abnormal
The main module begins by delcaring two wires, `flag` and `wrong`, that each hold 256 bits. From a programming perspective and for the purpose of solving this challenge, wires can be thought of as bit arrays. The flag is then passed to the `abnormal` module, with `wrong` being set to the output of the call. If `wrong` is set to all zeroes, then the flag is correct.

The 'abnormal' module concatenates the flag to a predefined string, which is then passed to `norc` and the result is stored in a wire named `w1`. Another predefined string is then passed to `norc` and the result is stored in a wire named `w2`. Then, using NOR operations, `w1` and `w2` are XOR'ed and the result is returned.

In pseudocode, `main` and `abnormal` would be something like this:
```Python
abnormal(flag):
    w1 = norc(predefined_str_1 + flag)
    w2 = norc(predefined_str_2)
    return w1 XOR w2

main():
    flag = 'ictf{__ENTER_FLAG_HERE__}'
    wrong = abnormal(flag)
    if wrong != 0:
        print 'wrong'
    else:
        print 'correct'
```

### NorC, NorB, & NorA
These three modules scramble the input passed to them by splitting, rearranging, and using NOR operations on their inputs. `norc` and `norb` operate more or less the same, with the key difference being that `norc` calls `norb` and `norb` calls `nora`. For the brute force solution I used, only `norc` is the only important module to understand out of these three. I cover the `norc` module in more detail further down, but here's a code snipped and pseudocode for some background:

Code:
```Verilog
module norc(out, in);
    output [256:0] out;
    input [512:0] in;

    norb n1({w1, out[15:0]}, {in[512], in[271:256], in[15:0]});
    norb n2({w2, out[31:16]}, {w1, in[31:16], in[287:272]});
    norb n3({w3, out[47:32]}, {w2, in[303:288], in[47:32]});
    ...
    norb n16({out[256], out[255:240]}, {w15, in[255:240], in[511:496]});
endmodule
```

Python-like Pseudocode:
```Python
norc(in):
    out = 257-bit array
    
    w1, out[15:0] = norb(in[512] + in[271:256] + in[15:0])
    w2, out[31:16] = norb(w1 + in[31:16] + in[287:272])
    w3, out[47:32] = norb(w2 + in[303:288] + in[47:32])
    ...
    out[256], out[255:240] = (w15 + in[255:240] + in[511:496])
    
    return out
```

## Initial Attempts
I attempted to solve this challenge a couple different ways before switching to a more direct brute-force method.

I first tried converting the Verilog code into Python, then modifying the Python code to brute force the flag one character at a time. However, this method failed for two main reasons:
  - Bit order errors - These came from two different sources:  
    - The Verilog code declares the wires, input, and outputs such that index 0 is the last element/least significant bit. For example, the declaration `input [512:0] in;` makes it such that `in[512]` is the first element/most significant bit and `in[0]` is the last element/least significant bit. Additionally, both indicies are inclusive, so in the case of `input [512:0] in;`, `in` is 513 bits long. While I didn't notice any index errors in my Python version of the code, I wouldn't be surprised if there were errors that I missed.
    - Unpacking lists in Python. In my Python code, I used `out[16-0], w1 = nora([args[32-32], args[32-16], args[32-0]])` to simulate the behavior of `nora n1({w1, out[0]}, {in[32], in[16], in[0]});` from the Verilog code. However, I had mixed up the order of the variables when writing the code without realizing it, so my initial Python code was `out[16-0], w1 = nora(...)`. This incorrect bit order not only caused rippled out to effect the rest of the final output, but was also present in all 16 calls to `nora` within the `norb` function.
  - Incorrectly brute forcing the flag. Even if my code had no logic errors and perfectly simulated the Verilog code, there was still the problem that I was brute forcing the flag incorrectly. As it turns out, the flag can only be brute forced from right to left, 1 to 16 bits at a time (this will be explained more later). Not only was I trying to brute force the flag from left to right, but the way I checked for progess was wrong as well.

I then tried reversing the logic of the Verilog code, but the ripple effects in the `norb` and `norc` functions made it way too tedious to fully reverse those functions.

## Successful Brute Force
For this solution, I decided to brute force the flag (again, one character at a time) by modifying the flag within Verilog source code, then compiling and running the modified code.
### Second Analysis
Before following through on this brute force attempt, I wanted to do two things:
  - Make sure the flag can be brute forced and what conditions, if any, need to be followed for a successful brute force
  - Find a way to know when we've got a character right and should move on to brute forcing the next character
 
I was able to verify that the flag can be brute forced just by looking at the `norc` module. The following is a line-by-line analysis of `norc`:
  - `input [512:0] in;`
    - `in[512:256]` is predefined, `in[255:0]` is the flag
  - `norb n1({w1, out[15:0]}, {in[512], in[271:256], in[15:0]});`
    - we know the value of `in[512]` and `in[271:256]` and we control the value of `in[15:0]`
    - `in[15:0]` is the last 16 bits of the flag, and `out[15:0]` is the last 16 bits of the output
  - `norb n2({w2, out[31:16]}, {w1, in[31:16], in[287:272]});`
    - `w1` creates a 'ripple' effect from the previous line
    - we control the value of `in[31:16]`, and we know the value of `in[287:272]`
    - `in[31:16]` is the last 16 bits of the flag, and `out[31:16]` is the last 16 bits of the output
  - this pattern repeats for the next 13 lines, where
    - `w_` causes a 'ripple' effect to each consecutive call of `norb`
    - each call to `norb` also uses a two 16-bit substrings: one we control (the flag) and one we know (predefined value prepended to the flag)
    - 16 bits of the output are set to the least significant 16 bits of the output from `norb`
  - this pattern changes slightly for the last line, where the only difference is
    - rather than a wire, `out[256]` is set to the most significant bit of the output of `norb`

Two important patterns emaerged from this second analysis:
  - `out[N+15:N]` corresponds to `in[N+15:N]`, meaning that changing bits 15-0 of the flag will change bits 15-0 of the output, changing bits 31-16 of the flag will change bits 31-16 of the output, and so on
    - Note: an analysis of `norb` shows a similar pattern, but instead of 16-bit chunks, it's each individual bit. This means changing bit X of the flag will change only bit X of the output (before considering output chaining).
  - Each call to `norb` is chained together such that changing bits 15-0 of the flag will change bits 255-16 of the output, changing bits 31-16 of the flag will change bits 255-32 of the output, and so on
    - Note: an analysis of `norb` shows a similar pattern, but instead it's calls to `nora` that are chained together.

Together, these two things mean we can brute force the flag 1 to 16 bits at a time from right to left. The flag must be brute forced from right to left because of the direction/order of the output chaining.

Finally, to provide the output needed for a brute force attack, the following code can be added to `abnormal` to print the module's output:
```Verilog
initial begin
    #10
    $display("%64H", out);
end
```
This will display the output of the `abnormal` module in hex. We can then check if the string ends in all zeroes to know how many (hex) characters of the flag are correct. If the output ends in N zeroes, we know that the last N (hex) characters of the flag are correct.

### Brute Forcing the Flag
To brute force the flag, I created a Python script to modify, compile, and run the Verilog code and use the output to brute force each (hex) character of the flag. The script makes use of the `subprocess` module to compile and run the code and retireve the output. The code is as follows:

```Python
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
```

Running this script, we get the flag `ictf{nero'ssonronrosenosoreores}` in hex.

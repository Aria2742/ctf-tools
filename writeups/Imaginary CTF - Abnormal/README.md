# Abnormal

## Files
 - [Makefile](./Makefile)
 - [abnormal.v](./abnormal.v)

## Description
For this challenges, we're provided with Verilog source code. The previous challenge, "Normal", included a makefile with the commands to compile and run the source code. The commands to compile and run the Verilog file are as follows:

compile: `iverilog -o normal.vvp -s main normal.v`  
run: `vvp normal.vvp`

## Initial Analysis
TODO - describe code...

## Initial Attempts
I attempted to solve this challenge a couple different ways before switching to a more direct brute-force method.

I first tried converting the Verilog code into Python, then modifying the Python code to brute force the flag. However, this method failed for two main reasons:
  - Bit order errors - These came from two different sources:  
    - The Verilog code declares the wires, input, and outputs such that index 0 is the last element/least significant bit. For example, the declaration `input [512:0] in;` makes it such that `in[512]` is the first element/most significant bit and `in[0]` is the last element/least significant bit. Additionally, both indicies are inclusive, so in the case of `input [512:0] in;`, `in` is 513 bits long. While I didn't notice any index errors in my Python version of the code, I wouldn't be surprised if there were errors that I missed.
    - Unpacking lists in Python. In my Python code, I used `out[16-0], w1 = nora([args[32-32], args[32-16], args[32-0]])` to simulate the behavior of `nora n1({w1, out[0]}, {in[32], in[16], in[0]});` from the Verilog code. However, I had mixed up the order of the variables when writing the code without realizing it, so my initial Python code was `out[16-0], w1 = nora(...)`. This incorrect bit order not only caused rippled out to effect the rest of the final output, but was also present in all 16 calls to `nora` within the `norb` function.
  - Incorrectly brute forcing the flag. Even if my code had no logic errors and perfectly simulated the Verilog code, there was still the problem that I was brute forcing the flag incorrectly. As it turns out, the flag can only be brute forced from right to left, at most 16 bits at a time (this will be explained more later). Not only was I trying to brute force the flag from left to right, but the way I checked for progess was wrong as well.

I then tried reversing the logic of the Verilog code, but the ripple effects in the `norb` and `norc` functions made it way too tedious to fully reverse those functions.

## Successful Brute Force

To do this, I first needed to make sure it was possible to brute force the flag and if it had to be brute forced in a certain order. Looking at 'abnormal.v', we see

```
module abnormal(out, in);
    output [255:0] out;
    input [255:0] in;

    wire [255:0] w1, w2, w3, w4, w5, w6;

    norc n1({c1, w1}, {257'h1a86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81, in});
	norc n2({c1, w2}, 513'h1a5e20394c934fd1198b1517d57e730cd225ccfa064ff42db76c19f3b7c0da91a6bf077b696cc4b22c0e56f4d3e6e150e386d6f04479ac502600e01fcdc29f5e4);
	...
```

The parameter 'in' is the flag, which we set in module 'main'. The curly brackets concatenate everything within them, meaning `{257'h1a86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81, in}` becomes `1a86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81________FLAG_BYTES_HERE_______...___`.

If we follow the function calls and look at `norc`, we see:
```
module norc(out, in);
    output [256:0] out;
    input [512:0] in;

    norb n1({w1, out[15:0]}, {in[512], in[271:256], in[15:0]});
    norb n2({w2, out[31:16]}, {w1, in[31:16], in[287:272]});
    norb n3({w3, out[47:32]}, {w2, in[303:288], in[47:32]});
    norb n4({w4, out[63:48]}, {w3, in[63:48], in[319:304]});
    norb n5({w5, out[79:64]}, {w4, in[335:320], in[79:64]});
    norb n6({w6, out[95:80]}, {w5, in[95:80], in[351:336]});
    norb n7({w7, out[111:96]}, {w6, in[367:352], in[111:96]});
    norb n8({w8, out[127:112]}, {w7, in[127:112], in[383:368]});
    norb n9({w9, out[143:128]}, {w8, in[399:384], in[143:128]});
    norb n10({w10, out[159:144]}, {w9, in[159:144], in[415:400]});
    norb n11({w11, out[175:160]}, {w10, in[431:416], in[175:160]});
    norb n12({w12, out[191:176]}, {w11, in[191:176], in[447:432]});
    norb n13({w13, out[207:192]}, {w12, in[463:448], in[207:192]});
    norb n14({w14, out[223:208]}, {w12, in[223:208], in[479:464]});
    norb n15({w15, out[239:224]}, {w14, in[495:480], in[239:224]});
    norb n16({out[256], out[255:240]}, {w15, in[255:240], in[511:496]});
endmodule
```
Additionally, both indices are inclusive and the order of the indices when variables are declared matters. In this case, index 512 is the first element/most significant bit of 'in'.

We can see that each call to `norb` has some trickle-down effect on each consecutive call of `norb`. This is done though the use of `w1`, `w2`, ... `w15`. However, the very first call to `norb` depends only on the input. The flag is stored at `in[255:0]`, and looking through the code, we can see the flag is read from right to left, 16 bits at a time. Because of the trickle-down effect, this means we need to brute-force the flag from right to left, attempting to brute-force no more than 16 bits at once.

The code abnormal_brute.py reads in abnormal.v, and creates a new file, abnormal_mod.v. The only change in this new file is that the flag is modified based on a brute-force attack. We've also added a #display statement to the Verilog code to make it print the result of `norc n1({c1, w1}, {257'h1a86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81, in});`. We can compare this against the result of `norc n2({c1, w2}, 513'h1a5e20394c934fd1198b1517d57e730cd225ccfa064ff42db76c19f3b7c0da91a6bf077b696cc4b22c0e56f4d3e6e150e386d6f04479ac502600e01fcdc29f5e4);` to check if the bits we're brute forcing are now equal. (We know they need to be equal since the logic in abnormal does an XOR operation between them, and the result needs to equal 0 - found this from previous attempt)

Run the script and we get the flag in hex, all that's left is to conver it to ascii

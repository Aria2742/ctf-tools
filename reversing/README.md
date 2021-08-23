# reversing
A collection of tools, scripts, and other info for reverse engineering

## Scripts
 - [nop_skipper.py](./nop_skipper.py)
   - de-obfuscates programs that contain large chunks of NOPs
   - created to deal with 71KB program that used huge chunks of NOPs between instructions, causing IDA and Ghidra to crash while disassembling
   - works by inserting `jmp` instructions to skip over large chunks of NOPs without disrupting relative addresses or other position-dependant structures
 - [brute_dict.py](./brute_dict.py)
   - reverses an encoding/encryption scheme by mapping inputs to outputs
   - useful for decoding stuff without needing to reverse the encoding/encryption process
   - works by using the encoding/encryption algorithm to build a dictionary in the format `(encoded_char, key) = decoded_char` then use the dictionary to decode a message

## Programs/Tools
 - [Ghidra](https://ghidra-sre.org/)
 - [IDA](https://hex-rays.com/ida-free/)
 - [HxD](https://mh-nexus.de/en/hxd/)
   - hex viewer/editor
 - [FileAlyzer2](https://www.safer-networking.org/products/filealyzer/)
   - useful for looking at executable header and section data
 - [dnSpy](https://github.com/dnSpy/dnSpy)
   - debugger and .NET assembly editor
   - can be used even if you don't have any source code available
 - [elparser](https://elfparser.com/)
   - basic ELF header/section analysis tool
   - can detect anti-RE techniques
 - [Cheat Engine](https://www.cheatengine.org/)
   - useful for modifying program values during runtime
 - [GameConqueror](https://github.com/scanmem/scanmem)
   - Linux equivalent of Cheat Engine
   - can be installed through apt
 - [NI LabView (Community Edition)](https://www.ni.com/en-us/support/downloads/software-products/download.labview.html#370001)
   - used for running and debugging .vi files
 - [OpenOffice](https://www.openoffice.org/)
   - collection of MS office-like programs
   - NI has plugins for viewing file formats associated with .vi files (such as TDMS files)
 - [cryptii](https://cryptii.com/)
   - modular conversion, encoding/decoding and encryption/decryption online
 - [JetBrains dotPeek](https://www.jetbrains.com/decompiler/)
   - decompiler for .NET programs

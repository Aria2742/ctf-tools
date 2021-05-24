# reversing
A collection of tools, scripts, and other info for reverse engineering

## Scripts
 - nop_skipper.py
   - de-obfuscates programs that contain large chunks of NOPs
   - created to deal with 71KB program that used huge chunks of NOPs between instructions, causing IDA and Ghidra to crash while disassembling
 - brute_dict.py
   - reverses an encoding/encryption scheme by mapping inputs to outputs
   - useful for decoding stuff without needing to reverse the encoding/encryption process

## Programs/Tools
 - Ghidra
 - IDA
 - HxD
   - hex viewer/editor
 - FileAlyzer2
   - useful for looking at executable header and section data
 - dnSpy
   - debugger and .NET assembly editor
   - can be used even if you don't have any source code available
 - elparser
   - basic ELF header/section analysis tool
   - can detect anti-RE techniques
 - Cheat Engine
   - useful for madifying program values during runtime
 - NI LabView
   - used for running and debugging .vi files
 - OpenOffice
   - collection of MS office-like programs
   - NI has plugins for viewing file formats associated with .vi files (such as TDMS files)
 - cryptii.com
   - modular conversion, encoding/decoding and encryption/decryption online

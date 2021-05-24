# name of executable with NOPs that need to be skipped
orig_bin = 'chall'
# name of executable with skipped NOPs to create
new_bin = 'chall_new'
# print % complete messages at least this % often
progress_percent = 5

# now we get into the code...

# read the data from the executable
orig = open(orig_bin, 'rb')
data = orig.read()
orig.close()

# create new file to write to
new = open(new_bin, 'wb')

# loop counter
idx = 0

# set up % progress stuff
checkpoint = len(data) // (100 // progress_percent)
prev_idx = 0

# function to check if there's a chunk of skippable NOPs
# size - size of chunk to check
#	if NOP chunk found, returned byte array is this size
# data - executable data
# idx - index to start reading data from
# returns byte array
#	if NOP chunk found, array is jmp followed by NOPs
#		jmp leads to end of NOP chunk
#	otherwise
#		return bytes(data[idx])
def chunk(size, data, idx):
	nops = data[idx:idx+size].count(0x90)
	if nops != size:
		return bytes([data[idx]])
	else:
		jmp_bytes = 5
		ret = bytearray(b'\xE9')
		ret.extend((size-jmp_bytes).to_bytes(4, byteorder='little'))
		for q in range(size-jmp_bytes):
			ret.extend(b'\x90')
		return ret

# read through all of data byte-by-byte
# if byte = 0x90, check for NOP chunk
while idx < len(data):
	if data[i] != 0x90: # not a NOP, just write to file
		new.write(bytes([data[idx]]))
		idx += 1
	else: # check for NOP chunk
		ret = []
		size = 0x80000 # starting NOP chunk size
		min_size = 16 # minimum chunk size (inclusive)
		# while NOP chunk not found and chunk size >= 16
		while len(ret) <= 1 and size >= min_size:
			ret = chunk(size, data, idx) # check for NOP chunk
			size = size // 2 # cut chunk size in half
		# write byte/NOP chunk to new file
		new.write(ret)
		idx += len(ret)
		
	# stuff for printing % progress
	if idx - prev_idx >= checkpoint:
		print(f'{idx*100//len(data)}% complete')
		prev_idx = idx

# print done and close files
print('done!')
new.close()
# encoded string to decode
encoded = 'c-n|TD^zJFp|I\'q"VCj7.mNj4'
# key used for encoding
key = 'f4|<eN3w$'
# dictionary used for decoding
# will be built as dict[(encoded_char, key)] = decoded_char
# leave this empty to start
decoder = {}

# function to build the decoder dictionary
# encodes all printable chars using each char of the key
# this function will need to be tweaked to fit your encoding algorithm
def build_dict():
	global decoder
	for k in key:
		for l in range(0x20, 0x7F): # all printable chars
			# change the following line(s) to be the encoding algorithm
			# DON'T reverse it to decode
			enc = ((l + ord(k) - 0x42) % 0x5F) + ord('!')
			# don't change the following line
			# this builds up the decoder dictionary
			decoder[(chr(enc), k)] = chr(l)

# decode the message using each char in the key
def decode():
	for k in key:
		dec = ''
		for l in encoded:
			dec += decoder[(l, k)]
		print(f'{k} : \'{dec}\'')

# run the code
build_dict()
decode()
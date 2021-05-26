#!/bin/env/python

import nclib

ip_addr = '206.189.121.131'
port = 30073

ciphertext = 'bb8f34e940bc192f32e20073bb3457ac53caf50faee79f6e455056bfd0ccfea638576b231cbff8756e43ad4015b1ddfca4b7eea5092509720c606f4326bedc58'
cipher_start = ciphertext[:32]
cipher_end = ciphertext[34:]
brute_byte = 0

got_flag = False

while not got_flag:
	# connect to the server
	nc = nclib.Netcat(connect=(ip_addr, port))

	# check prompt and send username
	response = str(nc.recv())
	if 'username' not in response:
		print('something messed up')
		print('expected \'username\', got \'' + response + '\'')
		quit()
	nc.send('admin')

	# check prompt and send password
	response = str(nc.recv())
	if 'password' not in response:
		print('something messed up')
		print('expected \'password\', got \'' + response + '\'')
		quit()
	nc.send('g0ld3nb0i')

	# check prompt and send forged ciphertext
	response = str(nc.recv())
	response = str(nc.recv())
	if 'ciphertext' not in response:
		print('something messed up')
		print('expected \'ciphertext\', got \'' + response + '\'')
		quit()
	brute_s = hex(brute_byte)[2:]
	if len(brute_s) == 1:
		brute_s = '0' + brute_s
	#print(cipher_start + brute_s + cipher_end)
	nc.send(cipher_start + brute_s + cipher_end)
	brute_byte += 1

	# check prompt and send forged ciphertext
	response = str(nc.recv())
	print(brute_s + ' - ' + response)
	if 'flag' in response:
		got_flag = True

	nc.close()
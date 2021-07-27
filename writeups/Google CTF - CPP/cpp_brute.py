"""
#warning - method to print???

def _LD(x, y):
	return ROM_x_y

def LD(x, y):
	return _LD(x, y)

def _MA(L0, L1, ..., L7):
	return L

def MA(L0, L1, ..., L7):
	return L

def l(...):
	return MA(...)
"""

ROM = [187, 85, 171, 197, 185, 157, 201, 105, 187, 55, 217, 205, 33, 179, 207, 207, 159, 9, 181, 61, 235, 127, 87, 161, 235, 135, 103, 35, 23, 37, 209, 27, 8, 100, 100, 53, 145, 100, 231, 160, 6, 170, 221, 117, 23, 157, 109, 92, 94, 25, 253, 233, 12, 249, 180, 131, 134, 34, 66, 30, 87, 161, 40, 98, 250, 123, 27, 186, 30, 180, 179, 88, 198, 243, 140, 144, 59, 186, 25, 110, 206, 223, 241, 37, 141, 64, 128, 112, 224, 77, 28]

alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_{}'
#FLAG = 'CTF{write_flag_here_please}'

def LD(L):
	#print(f'DEBUG: Attempting access at {hex(L)}')
	if L >= 0 and L <= 0x5A:
		return ROM[L]
	elif L >= 0x80 and L <= 0x9A:
		return ord(FLAG[L-0x80])
	else:
		#print('ERROR: ACCESS AT INVALID ADDRESS') 
		return -1

TARGET_I = 25
for letter in alpha:
	FLAG = 'CTF{pr3pr0cess0r_pr0fe5so' + letter + '}' # letter 25 is 'r'
	S = 0
	R = 0
	Z = 0
	A = 0
	B = 0
	L = 0
	Y = 0
	X = 0
	Q = 0
	I = 0
	N = 1
	M = 0
	O = 0
	P = 0
	while(True):
		if S == 0:
			#print(f'S = {S}')
			S = 24
		if S == 1:
			#print(f'S = {S}')
			S = 2
			R = ~R & 0xFF
		if S == 2:
			#print(f'S = {S}')
			S = 3
			Z = 1
		if S == 3:
			#print(f'S = {S}')
			S = 4
			R = (R + Z) & 0xFF
		if S == 4:
			#print(f'S = {S}')
			S = 5
			R = (R + Z) & 0xFF
		if S == 5:
			#print(f'S = {S}')
			S = 6
			if R == 0:
				S = 38
		if S == 6:
			#print(f'S = {S}')
			S = 7
			R = R + Z
		if S == 7:
			#print(f'S = {S}')
			S = 8
			if R == 0:
				S = 59
		if S == 8:
			#print(f'S = {S}')
			S = 9
			R = (R + Z) & 0xFF
		if S == 9:
			#print(f'S = {S}')
			S = 10
			if R == 0:
				S = 59
		if S == 10:
			#print(f'S = {S}')
			S = 11
			#print("ERROR: BUG")
			break
		if S == 11:
			#print(f'S = {S}')
			S = 12
			S = -1
		if S == 12:
			#print(f'S = {S}')
			S = 13
			X = 1
		if S == 13:
			#print(f'S = {S}')
			S = 14
			Y = 0
		if S == 14:
			#print(f'S = {S}')
			S = 15
			if X == 0:
				S = 22
		if S == 15:
			#print(f'S = {S}')
			S = 16
			Z = X
		if S == 16:
			#print(f'S = {S}')
			S = 17
			Z = (Z & B) & 0xFF
		if S == 17:
			#print(f'S = {S}')
			S = 18
			if Z == 0:
				S = 19
		if S == 18:
			#print(f'S = {S}')
			S = 19
			Y = (Y + A) & 0xFF
		if S == 19:
			#print(f'S = {S}')
			S = 20
			X = (X + X) & 0xFF
		if S == 20:
			#print(f'S = {S}')
			S = 21
			A = (A + A) & 0xFF
		if S == 21:
			#print(f'S = {S}')
			S = 14
		if S == 22:
			#print(f'S = {S}')
			S = 23
			A = Y
		if S == 23:
			#print(f'S = {S}')
			S = 1
		if S == 24:
			#print(f'S = {S}')
			S = 25
			I = 0
		if S == 25:
			#print(f'S = {S}')
			S = 26
			M = 0
		if S == 26:
			#print(f'S = {S}')
			S = 27
			N = 1
		if S == 27:
			#print(f'S = {S}')
			S = 28
			P = 0
		if S == 28:
			#print(f'S = {S}')
			S = 29
			Q = 0
		if S == 29:
			#print(f'S = {S}')
			S = 30
			B = 0xE5
		if S == 30:
			#print(f'S = {S}')
			S = 31
			B = (B + I) & 0xFF
		if S == 31:
			#print(f'S = {S}')
			S = 32
			if B == 0:
				S = 56
		if S == 32:
			#print(f'S = {S}')
			S = 33
			B = 0x80
		if S == 33:
			#print(f'S = {S}')
			S = 34
			B = (B + I) & 0xFF
		if S == 34:
			#print(f'S = {S}')
			S = 35
			L = B
			##print('Access from S == 34')
			A = LD(L)
		if S == 35:
			#print(f'S = {S}')
			S = 36
			L = I
			##print('Access from S == 35')
			B = LD(L)
		if S == 36:
			#print(f'S = {S}')
			S = 37
			R = 1
		if S == 37:
			#print(f'S = {S}')
			S = 12
		if S == 38:
			#print(f'S = {S}')
			S = 39
			O = M
		if S == 39:
			#print(f'S = {S}')
			S = 40
			O = (O + N) & 0xFF
		if S == 40:
			#print(f'S = {S}')
			S = 41
			M = N
		if S == 41:
			#print(f'S = {S}')
			S = 42
			N = O
		if S == 42:
			#print(f'S = {S}')
			S = 43
			A = (A + M) & 0xFF
		if S == 43:
			#print(f'S = {S}')
			S = 44
			B = 0x20
		if S == 44:
			#print(f'S = {S}')
			S = 45
			B = (B + I) & 0xFF
		if S == 45:
			#print(f'S = {S}')
			S = 46
			L = B
			##print('Access from S == 45')
			C = LD(L)
		if S == 46:
			#print(f'S = {S}')
			S = 47
			A = (A ^ C) & 0xFF
		if S == 47:
			#print(f'S = {S}')
			S = 48
			P = (P + A) & 0xFF
		if S == 48:
			#print(f'S = {S}')
			S = 49
			B = 0x40
		if S == 49:
			#print(f'S = {S}')
			S = 50
			B = (B + I) & 0xFF
		if S == 50:
			#print(f'S = {S}')
			S = 51
			L = B
			##print('Access from S == 50')
			A = LD(L)
		if S == 51:
			#print(f'S = {S}\t\tP = {P}')
			S = 52
			A = (A ^ P) & 0xFF
		if S == 52:
			#print(f'S = {S}')
			if A == 0:# and I == TARGET_I:
				print(f'A == 0 using flag \'{FLAG}\' at I = {I}')
			S = 53
			Q = (Q | A) & 0xFF
		if S == 53:
			#print(f'S = {S}')
			S = 54
			A = 1
		if S == 54:
			#print(f'S = {S}')
			S = 55
			I = (I + A) & 0xFF
		if S == 55:
			#print(f'S = {S}')
			S = 29
		if S == 56:
			#print(f'S = {S}')
			S = 57
			if Q == 0:
				S = 58
		if S == 57:
			#print(f'S = {S}')
			S = 58
			#print("ERROR: INVALID FLAG")
			break
		if S == 58:
			#print(f'S = {S}')
			S = -1
			#print("SUCCESS: VALID FLAG")
			break
		#print(f'\tI = {I}')
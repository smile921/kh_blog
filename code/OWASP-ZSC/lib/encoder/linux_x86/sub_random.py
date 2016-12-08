#!/usr/bin/env python
'''
OWASP ZSC | ZCR Shellcoder
https://www.owasp.org/index.php/OWASP_ZSC_Tool_Project
https://github.com/Ali-Razmjoo/OWASP-ZSC
http://api.z3r0d4y.com/
https://lists.owasp.org/mailman/listinfo/owasp-zsc-tool-project [ owasp-zsc-tool-project[at]lists[dot]owasp[dot]org ]
'''
import random,binascii,string
from core.compatible import version
_version = version()
chars = string.digits + string.ascii_letters
def start(shellcode,job):
	if 'chmod' == job:	
		t = True
		eax = str('0x0f')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False
		eax = 'push   $%s'%(str(eax))
		eax_sub = 'push $0x%s\npop %%eax\npush $0x%s\npop %%ebx\nsub %%eax,%%ebx\npush %%ebx\n'%(eax_1,eax_2)
		shellcode = shellcode.replace(eax,eax_sub)
		ecx = str(shellcode.rsplit('\n')[8])
		ecx_value = str(shellcode.rsplit('\n')[8].rsplit()[1][1:])
		t = True
		while t:
			if _version is 2:
				ecx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
			if _version is 3:
				ecx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
			ecx_2 = "%x" % (int(ecx_value, 16) + int(ecx_1, 16))
			if '00' not in str(ecx_1) and '00' not in str(ecx_2) and len(ecx_1) >= 7 and len(ecx_2) >= 7:
				t = False
		ecx_sub = 'push $0x%s\npop %%ebx\npush $0x%s\npop %%ecx\nsub %%ecx,%%ebx\npush %%ebx\n\n'%(str(ecx_2),str(ecx_1))
		shellcode = shellcode.replace(ecx,ecx_sub)
		n = 0
		start = ''
		middle = ''
		end = ''
		sub = 0
		for l in shellcode.rsplit('\n'):
			n += 1
			if sub is 0:
				if '_z3r0d4y_' not in l:
					start += l + '\n'
				else:
					sub = 1
			if sub is 1:
				if '_z3r0d4y_' not in l:
					if '%esp,%ebx' not in l:
						middle += l + '\n'
					else:
						sub = 2
			if sub is 2:
				end += l + '\n'
		for l in middle.rsplit('\n'):
			t = True
			while t:
				if 'push $0x' in l:
					ebx = l.rsplit()[1][1:]
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(ebx[2:], 16) + int(ebx_1, 16))
					if '00' not in str(ebx_1) and '00' not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%edx\nsub %%ebx,%%edx\npush %%edx\n'%(str(ebx_1),str(ebx_2))
						middle = middle.replace(l,command)
						t = False
				else:
					t = False
		shellcode = start + middle + end
	elif 'dir_create' == job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'download_execute' == job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'download' == job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'exec' == job:
		t = True
		eax = str('0x46')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False

		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('mov    $0x46,%al',eax_sub)	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2.replace('-','')) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False


	elif 'file_create' == job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '00' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'script_executor' == job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '0' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'system' in job:
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		t = True
		eax = str('0xb')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax>eax_1:
				if '00' not in str(eax_1) and '0' not in str(eax_2):
					t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd',eax_sub+'\ncltd\n')	
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					if _version is 2:
						ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
					if _version is 3:
						ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
	elif 'write' in job:
		t = True
		eax = str('0x5')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax_1 != eax:
				if eax>eax_1:
					if '00' not in str(eax_1) and '0' not in str(eax_2):
						t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0x5\npop    %eax',eax_sub)
		
		t = True
		eax = str('0x4')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(1)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(1))).encode('latin-1'))).decode('latin-1')
			eax_1 = str('0') + str(eax_1[1])
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax_1 != eax:
				if eax>eax_1:
					if str('00') not in str(eax_1) and str('0') not in str(eax_2):
						t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0x4\npop    %eax',eax_sub)
		A = 0

		for line in shellcode.rsplit('\n'):
			if 'mov    %esp,%ebx' in line:
				A = 1
				shellcode = shellcode.replace(line,'\nmov    %esp,%ebx\n_z3r0d4y_\n')
			if A is 0:
				if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
					data = line.rsplit('push')[1].rsplit('$0x')[1]
					t = True
					while t:
						if _version is 2:
							ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
						if _version is 3:
							ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
						ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
						if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1 and ebx_1 != data:
							if '-' in ebx_2:
								ebx_2 = ebx_2.replace('-','')
								command = '\npush $0x%s\npop %%ebx\nneg %%ebx\nsub $0x%s,%%ebx\npush %%ebx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
							if t is True:
								command = '\npush $0x%s\npop %%ebx\nsub $0x%s,%%ebx\npush %%ebx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
		shellcode = shellcode.replace('_z3r0d4y_','')
		
		t = True
		eax = str('4014141')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if eax_1 != eax:
				if eax>eax_1:
					if '00' not in str(eax_1) and '00' not in str(eax_2):
						t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%ecx\nneg %%ecx\nsub $0x%s,%%ecx\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%ecx\nsub $0x%s,%%ecx\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0x4014141\npop    %ecx',eax_sub+'\n_z3r0d4y_\n').replace('mov %esp,%ecx','\n_z3r0|d4y_\nmov %esp,%ecx\n')
		A = 1
		for line in shellcode.rsplit('\n'):
			if '_z3r0d4y_' in line:
				A = 0
			if '_z3r0|d4y_' in line:
				A = 2
			if A is 0:
				if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
					data = line.rsplit('push')[1].rsplit('$0x')[1]
					t = True
					while t:
						if _version is 2:
							ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
						if _version is 3:
							ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
						ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
						if ebx_1 != data and str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
							if '-' in ebx_2:
								ebx_2 = ebx_2.replace('-','')
								command = '\npush $0x%s\npop %%ecx\nneg %%ecx\nsub $0x%s,%%ecx\npush %%ecx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
							if '-' not in ebx_2 and t is True:
								command = '\npush $0x%s\npop %%ecx\nsub $0x%s,%%ecx\npush %%ecx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
			if A is 2:
				if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
					data = line.rsplit('push')[1].rsplit('$0x')[1]
					t = True
					while t:
						if _version is 2:
							ebx_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
						if _version is 3:
							ebx_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
						ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
						if ebx_1 != data and str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
							if '-' in ebx_2:
								ebx_2 = ebx_2.replace('-','')
								command = '\npush $0x%s\npop %%edx\nneg %%edx\nsub $0x%s,%%edx\npush %%edx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
							if '-' not in ebx_2 and t is True:
								command = '\npush $0x%s\npop %%edx\nsub $0x%s,%%edx\npush %%edx\n'%(str(ebx_2),str(ebx_1))
								shellcode = shellcode.replace(line,command)
								t = False
		shellcode = shellcode.replace('_z3r0d4y_','').replace('_z3r0|d4y_','')
		t = True
		eax = str('0b909090')
		while t:
			if _version is 2:
				eax_1 = binascii.b2a_hex(''.join(random.choice(chars) for i in range(4)))
			if _version is 3:
				eax_1 = (binascii.b2a_hex((''.join(random.choice(chars) for i in range(4))).encode('latin-1'))).decode('latin-1')
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if '00' not in str(eax_1) and '00' not in str(eax_2) and eax_1 != eax:
				t = False
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%edx\nneg %%edx\nsub $0x%s,%%edx\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%edx\nsub $0x%s,%%edx\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push $0x0b909090\n\npop %edx\n',eax_sub)
	return shellcode

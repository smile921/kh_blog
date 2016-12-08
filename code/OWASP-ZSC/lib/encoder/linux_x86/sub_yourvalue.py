#!/usr/bin/env python
'''
OWASP ZSC | ZCR Shellcoder
https://www.owasp.org/index.php/OWASP_ZSC_Tool_Project
https://github.com/Ali-Razmjoo/OWASP-ZSC
http://api.z3r0d4y.com/
https://lists.owasp.org/mailman/listinfo/owasp-zsc-tool-project [ owasp-zsc-tool-project[at]lists[dot]owasp[dot]org ]
'''
def start(type,shellcode,job):
	if 'chmod' == job:	
		t = True
		eax = str('0x0f909090')
		while t:
			eax_1 = type.rsplit('sub_')[1][2:]
			eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
			if '00' not in str(eax_1) and '00' not in str(eax_2):
				t = False
		eax = 'push   $0x0f'
		eax_xor = 'push $0x%s\npop %%eax\npush $0x%s\npop %%ebx\nsub %%eax,%%ebx\nshr $0x10,%%ebx\nshr $0x08,%%ebx\npush %%ebx\n'%(eax_1,eax_2)
		shellcode = shellcode.replace(eax,eax_xor)
		ecx = str(shellcode.rsplit('\n')[10])
		ecx_value = str(shellcode.rsplit('\n')[10].rsplit()[1][1:])
		t = True
		while t:
			ecx_1 = type.rsplit('sub_')[1][2:]
			ecx_2 = "%x" % (int(ecx_value, 16) + int(ecx_1, 16))
			if '00' not in str(ecx_1) and '00' not in str(ecx_2) and len(ecx_1) >= 7 and len(ecx_2) >= 7 and '-' not in ecx_2:
				t = False
		ecx_xor = 'push $0x%s\npop %%ebx\npush $0x%s\npop %%ecx\nsub %%ebx,%%ecx\npush %%ecx\n_z3r0d4y_\n'%(str(ecx_1),str(ecx_2))
		shellcode = shellcode.replace(ecx,ecx_xor)
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
					ebx_1 = type.rsplit('sub_')[1][2:]
					ebx_2 = "%x" % (int(ebx[2:], 16) + int(ebx_1, 16))
					if '00' not in str(ebx_1) and '00' not in str(ebx_2) and '-' not in ebx_2 and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%edx\nsub %%ebx,%%edx\npush %%edx\n'%(str(ebx_1),str(ebx_2))
						middle = middle.replace(l,command)
						t = False
				else:
					t = False
		shellcode = start + middle + end
	elif 'dir_create' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	

		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'download_execute' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	

		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'download' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	

		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'exec' == job:
		value = str(type.rsplit('sub_')[1][2:])
		t = True
		eax = str('0x46909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n_z3r0d4y_'%(eax_2,eax_1)

		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n_z3r0d4y_'%(eax_2,eax_1)
		shellcode = shellcode.replace('mov    $0x46,%al',eax_sub)	
		A = 0
		for line in shellcode.rsplit('\n'):
			if '_z3r0d4y_' in line:
				A = 1
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14 and A is 1:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				t = True
				while t:
					ebx_1 = value
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						ebx_2 = ebx_2.replace('-','')
						command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
						shellcode = shellcode.replace(line,command)
						t = False
		shellcode = shellcode.replace('_z3r0d4y_','')
	elif 'file_create' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	

		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'script_executor' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	

		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'system' == job:
		value = str(type.rsplit('sub_')[1][2:])
		shellcode = 'xor %edx,%edx\n' + shellcode.replace('push   $0xb\npop    %eax\ncltd','').replace('push   %ebx\nmov    %esp,%ecx','push   %ebx\nmov    %esp,%ecx'+'\n'+'push   $0xb\npop    %eax\ncltd')
		
		for line in shellcode.rsplit('\n'):
			if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
				data = line.rsplit('push')[1].rsplit('$0x')[1]
				ebx_1 = value
				ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
				A = 0
				if str('-') in str(ebx_2):
					ebx_2 = ebx_2.replace('-','')
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nneg %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
					A = 1
				if A is 0:
					command = '\npush $0x%s\npop %%ebx\npush $0x%s\npop %%eax\nsub %%ebx,%%eax\npush %%eax\n'%(str(ebx_1),str(ebx_2))
				shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('push   $0xb\npop    %eax\ncltd','push   $0xb909090\npop    %eax\ncltd')
		eax = str('0xb909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0xb909090\npop    %eax\ncltd',eax_sub+'\ncltd\n')
	elif 'write' == job:
		value = str(type.rsplit('sub_')[1][2:])
		eax = str('0x5909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0x5\npop    %eax',eax_sub)
		eax = str('0x4909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
		A = 0	
		eax = 'push   $%s'%(str(eax))	
		if '-' in eax_2:
			A = 1
			eax_2 = eax_2.replace('-','')
			eax_sub = 'push $0x%s\npop %%eax\nneg %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		if A is 0:
			eax_sub = 'push $0x%s\npop %%eax\nsub $0x%s,%%eax\nshr $0x10,%%eax\nshr $0x08,%%eax\n'%(eax_2,eax_1)
		shellcode = shellcode.replace('push   $0x4\npop    %eax',eax_sub)
		A = 0
		for line in shellcode.rsplit('\n'):
			if 'mov    %esp,%ebx' in line:
				A = 1
				shellcode = shellcode.replace(line,'\nmov    %esp,%ebx\n_z3r0d4y_\n')
			if A is 0:
				if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
					data = line.rsplit('push')[1].rsplit('$0x')[1]
					ebx_1 = value
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					if str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1 and ebx_1 != data:
						if '-' in ebx_2:
							ebx_2 = ebx_2.replace('-','')
							command = '\npush $0x%s\npop %%ebx\nneg %%ebx\nsub $0x%s,%%ebx\npush %%ebx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)
					
						if '-' not in ebx_2:
							command = '\npush $0x%s\npop %%ebx\nsub $0x%s,%%ebx\npush %%ebx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)
		shellcode = shellcode.replace('_z3r0d4y_','')
		eax = str('4014141')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
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
					ebx_1 = value
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					if ebx_1 != data and str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						if '-' in ebx_2:
							ebx_2 = ebx_2.replace('-','')
							command = '\npush $0x%s\npop %%ecx\nneg %%ecx\nsub $0x%s,%%ecx\npush %%ecx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)
						if '-' not in ebx_2:
							command = '\npush $0x%s\npop %%ecx\nsub $0x%s,%%ecx\npush %%ecx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)
			if A is 2:
				if 'push' in line and '$0x' in line and ',' not in line and len(line) > 14:
					data = line.rsplit('push')[1].rsplit('$0x')[1]
					ebx_1 = value
					ebx_2 = "%x" % (int(data, 16) + int(ebx_1, 16))
					if ebx_1 != data and str('00') not in str(ebx_1) and str('00') not in str(ebx_2) and len(ebx_2) >=7 and len(ebx_1) >= 7 and '-' not in ebx_1:
						if '-' in ebx_2:
							ebx_2 = ebx_2.replace('-','')
							command = '\npush $0x%s\npop %%edx\nneg %%edx\nsub $0x%s,%%edx\npush %%edx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)
						if '-' not in ebx_2:
							command = '\npush $0x%s\npop %%edx\nsub $0x%s,%%edx\npush %%edx\n'%(str(ebx_2),str(ebx_1))
							shellcode = shellcode.replace(line,command)

		shellcode = shellcode.replace('_z3r0d4y_','').replace('_z3r0|d4y_','')
		t = True
		eax = str('0b909090')
		eax_1 = value
		eax_2 = "%x" % (int(eax, 16) + int(eax_1, 16))
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

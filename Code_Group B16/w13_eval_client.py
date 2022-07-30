## Step 1:

# Import module.
import os
import sys

import socket

import time

import random
import base64
from Crypto.Cipher import AES

if len(sys.argv) != 4:
    print('Invalid number of arguments')
    print('python eval_server.py [IP address] [Port] [groupID]')
    sys.exit()

ip_addr = sys.argv[1]
port_num = int(sys.argv[2])
group_id = sys.argv[3]

#file = open("/home/xilinx/jupyter_notebooks/CommsExternal/write_prediction.txt", "w").close()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip_addr, port_num)
print ('[+] Connecting to %s Port %s' % server_address)
sock.connect(server_address)
print('1fc394163ee2e70ad768b72ab23e83a3')

## Read writeOffset and calculate sync
def sync_calculate():
    maxTime = 0
    minTime = 0
    
    my_array = [0,0,0]
    
    f1 = open('write_offset01.txt', "r")
    time01 = f1.readlines()
    
    for x in time01:
        if x != '':
            x = float(x.rstrip())
   
    my_array[0] = max(time01)
    print ('max01 = %s' % my_array[0] )
    
    f2 = open('write_offset02.txt', "r")
    time02 = f2.readlines()
    
    for y in time02:
        y = float(y.rstrip())

    my_array[1] = max(time02)
    print ('max02 = %s' % my_array[1] )
    
    f3 = open('write_offset03.txt', "r")
    time03 = f3.readlines()
    
    for z in time03:
        z = float(z.rstrip())
    
    my_array[2] = max(time03)
    print ('max03 = %s' % my_array[2] )
    
    maxTime = max(my_array)
    print ('maxTime = %s' % maxTime)
    minTime = min(my_array)
    print ('minTime = %s' % minTime)
    sync = float(maxTime) - float(minTime)
    
    open('write_offset01.txt', "w").close()
    open('write_offset02.txt', "w").close()
    open('write_offset03.txt', "w").close()
    
    return int( sync*1000 )

## Encrypt message sent by TCP/IP Client
def encrypt_message(plain_text):
    secret_key = '1fc394163ee2e70ad768b72ab23e83a3'
    
    iv = os.urandom(16)
    
    plain_text = plain_text.replace( '\n', '' )
    
    plain_text = '#' + plain_text;
    print('[+] ' + plain_text)
    
    aes = AES.new(secret_key, AES.MODE_CBC, iv)   
    
    if len(plain_text)%16 != 0:
        plain_text = plain_text.ljust(32, '0')
        print('[+] ' + plain_text)
    else:
        pass
    
    encrypted_data = aes.encrypt(plain_text)
    
    encoded_data = base64.b64encode(iv + encrypted_data)
    
    return encoded_data

## Step 2:

from time import sleep

try:
    # Send data 01
    print ( '[+] Start Dancing!')

    prv_count = 0
    
    while True:
        sleep(0.1)

        line_count = 0
        file = open('/home/xilinx/jupyter_notebooks/Overlays/Week13/output.txt', "r")
        Lines = file.readlines()
        file.close()

        for line in Lines:
            line_count += 1
            message = line.strip()
        
        if (line_count > prv_count): 
            print ( '[+] Sending "%s"' % message )

            sync = sync_calculate()
            
            sock.sendto(encrypt_message(message + '|' + str(sync) + '.'),(server_address))
            
            data = sock.recv(1024)
            print ( '[+] Received "%s"' % data )
            data = str(data)
            pos = data[2:7]
            filePos = open('/home/xilinx/jupyter_notebooks/Overlays/Week13/positions.txt', "a+")
            filePos.seek(0)
            check = filePos.read(5)
            if len(check) > 0:
                filePos.write("\n")
            filePos.write(pos)
            filePos.close()
            print ( '[+] Start Dancing!')
            prv_count = line_count
    
finally:
    print ('[-] closing socket')
    sock.close()

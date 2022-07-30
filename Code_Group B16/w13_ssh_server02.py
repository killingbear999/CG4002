## Step 1:

import sys

import ntplib
import time
from time import ctime
import os

# Import module
import socket

if len(sys.argv) != 2:
        print('Invalid number of arguments')
        print('python3 practice_ssh_client.py [Port]')
        sys.exit()

port_num = int(sys.argv[1])

global tc0, tc3, ts1, ts2
global timeOffset, roundTripTime

TEST = "D:/Documents/Modules/Sem_05/CG4002/Comms/test_input.txt"
ACTUAL = "/home/xilinx/jupyter_notebooks/Overlays/Week13/input2.txt"
ACK = 'ACK'

file = open(ACTUAL, "w").close()
file02 = open("/home/xilinx/jupyter_notebooks/CommsExternal/write_offset02.txt", "w").close()


c = ntplib.NTPClient()

response = c.request('asia.pool.ntp.org', version=3)

def getActualTime():
    return time.time() + response.offset

def parse_message(data):
    global ts1, tc0
    ts1 = getActualTime()
    decoded_data = data.decode()
    messages = decoded_data.split('/')
    message, time0, time3 = messages[:3]
    tc0 = time0
    return {
        'message': message, 'time0': float(time0) ,'time3': float(time3)
    }

def parse_ACK(data):
    global tc3
    decoded_data = data.decode()
    messages = decoded_data.split('/')
    message, time0, time3 = messages[:3]
    tc3 = time0
    
def timestamp_message(message):
    global ts2
    ts2 = getActualTime()

def time_offset(): 
    global tc0, tc3, ts2, ts1, timeOffset, roundTripTime
    ts2 = getActualTime()
    tc3 = getActualTime()
    roundTripTime = ( ts1 - float(tc0) ) - ( ts2 - float(tc3) )
    print('[+] roundTripDelay : %s' % roundTripTime)
    clockOffset = ts1 - float(tc0) - ( roundTripTime / 2 )
    print('[+] clockOffset : %s' % clockOffset)
    
    return getActualTime() + clockOffset
    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Step 2:

# IP and port for accepting connections
server_address = ('localhost', port_num)

# Print server address and port
print("[+] Server IP {} | Port {}".format(server_address[0], server_address[1]))

# Bind socket with server
sock.bind(server_address)

## Step 3:

# Listen for incoming connections
sock.listen(1)

# Create Loop
while True:
    # Wait for a connections
    print ('[+] Waiting for a client connection')
    
    # Connection established
    connection, client_address = sock.accept()
    
    ## Step 4:
    
    try:
        print ('[+] Connection from', client_address)
        
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            
            print( 'received "%s"' % ( ( data.decode() ).rstrip() ) )
            
            if ( ( data.decode().rstrip() ).__contains__( 'Start movement' ) ):
                #time.sleep(1)
                parsed_message = parse_message(data)
                
                clockOffset = time_offset( )
                
                with open("/home/xilinx/jupyter_notebooks/CommsExternal/write_offset02.txt", "a") as f:
                    f.write( str(clockOffset) + '\n')
                
                file = open(ACTUAL, "w").close()
            
            else:
                file = open(ACTUAL, "a")
                #file.write( ( data.decode() ).replace( '\r' , '' ))
                file.write(data.decode())


    finally:
        # Close the connection
        connection.close()


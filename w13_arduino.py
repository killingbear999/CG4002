import sys
import ntplib
import serial
import time
import socket

if len(sys.argv) != 2:
        print('Invalid number of arguments')
        print('python3 practice_ssh_client.py [Port]')
        sys.exit()

port_num = int(sys.argv[1])

c = ntplib.NTPClient()

global tc0, tc2, tc3, tc4, sock

#file1 = open("ReadTest.txt", "r")

response = c.request('asia.pool.ntp.org', version=3)

def getActualTime():
    return time.time() + response.offset

def decrypt_message(data):
    decoded_data = data.decode()
    messages = decoded_data.split('/')
    message, time1, time2 = messages[:3]
    return {
        'message': message, 'time1': time1, 'time2': time2
    }
    
def timestamp_message(message):
    global amount_received
    global tc0, tc3
    tc0 = getActualTime()
    timestampMessage = str(message) + '/' + str(tc0)
    #if (amount_received == 0):
        #timestampMessage = timestampMessage + '/' + str(0)
    timestampMessage = timestampMessage + '/' + str(0) + '/'
    #else:
        #timestampMessage = timestampMessage + '/' + str(tc3)
    #print("[+] timestamped message = " + timestampMessage)
    return timestampMessage

def time_offset(serverTime1, serverTime2):
    global tc0, tc3
    tc3 = getActualTime()
    timeOffset = abs((( float(serverTime1) - tc0 ) + ( float(serverTime2) - tc3 )) / 2)
    print('[+] timeOffset : %s' % timeOffset)
    roundTripDelay = ( tc3 - tc0 ) - ( float(serverTime2) - float(serverTime1) )
    print('[+] roundTripDelay : %s' % roundTripDelay)

    
def create_connect_socket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', port_num)
    print ('[+] Connecting to %s Port %s' % server_address)
    sock.connect(server_address)
    return sock


bluno1 = serial.Serial("/dev/cu.usbmodem14101", 9600, timeout = 1)
#bluno2 = serial.Serial("COM9", 9600, timeout = 1)
c = [0, 0, 0]
t = [0, 0, 0]

def retrieveData(device):
    try:
        if device == 1:
            bluno1.write(b'1')
            data = bluno1.readline().decode('ascii')
        return data
    except SerialTimeoutException:
        t[device-1] += 1
        if(t[device-1] == 5):
            c[device-1] = 0
            return "disconnected"
        return "timeout"

def sendData(data):
    global sock

    if ( data.__contains__('Start movement') ):
        data = timestamp_message(data) + '\n'
    
    print ('[+] Sending "%s"' % data)
    sock.sendall(data.encode())

def dataCleaning(rawData): 
    partitions = rawData.count(",")
    if partitions == 5:
        array = rawData.split(",")
        for num in array:
            x = num
            if x == "" or x.count(".") > 1 or x.count("-") > 1:    
                return False
        return True
    elif rawData.strip() == "Start movement":
        return True
    else:  
        return False
    

def main():
    global sock
    sock = create_connect_socket()
    time.sleep(0.01)
        
    while(True):
        device = 1
        data = str(retrieveData(device))
        clean = dataCleaning(data)

        if data != "":
            if clean:
                sendData(data)         
        else:
            print("No data received")
            time.sleep(0.1)

if __name__ == "__main__":
    main()

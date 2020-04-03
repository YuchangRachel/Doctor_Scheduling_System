#!/usr/bin/env python

import socket

def main():
    port=21000
    host='127.0.0.1'
    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #open TCP connection to hostname on the port
    clientsocket.connect((host, port))

    print "Phase1: Patient2 has TCP port number:", clientsocket.getsockname()[1], "and IP Address:", clientsocket.getsockname()[0]

    #read patient1.txt
    with open('input/patient2.txt', 'r') as f:
        store=f.read()

    list=store.split()
    print 'Phase1: Authentication request from Patient2 with username', list[0], 'and password', list[1], 'has been sent to the Health Center Server'

    #communication
    clientsocket.send(store)
    reply=clientsocket.recv(1024)
    print ("Phase1: Patient2 authentication result: %s" % (reply))
    print '-----Phase1: End of Phase1 Authentication for Patient2.-----'

    #(must success in Phase1)Phase2: ask for availability
    if reply == "Success":
        ask='available'
        clientsocket.send(ask)
        print "send",ask
    
        #receive available time schedule
        time=clientsocket.recv(1024)
        print 'Phase2: The following appointments are available for patient2:\n', time
        while 1:
            print 'Please enter the preferred appointment index and press enter:'
            i=raw_input()
            prefer='selection ' + i 
            clientsocket.send(prefer)
            result=clientsocket.recv(1024)
            if result != 'invalid':
                break

        if result == 'notavailable':
            print 'Phase2: The requested appointment from Patient2 is not available.Exiting'
            clientsocket.close()
        else:
            print 'Phase2: The requestd appointment is available and reserved to Patient2. The assigned doctor name & port number is', result
            clientsocket.close()
            #--------------Phase3----------------
            #dynamically connect to doctor port
            udpport=int(result)
            address=('127.0.0.1', udpport)
            udpsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsocket.connect((address))

            print "Phase3: Patient2 has a dynamic UDP port number:", udpsocket.getsockname()[1], "and IP Address:", udpsocket.getsockname()[0]
            #read my own insuance plan
            try:
                with open('input/patient2insurance.txt', 'r') as f:
                    insurance=f.read()
                print 'My insurance:', insurance
            except IOError:
                print 'FIle is not found'
                udpsocket.close()
                sys.exit(1)
            #catch doc port and IP address
            #send to certerin port
            name='Patient2'
            udpsocket.sendto(name, address)
            udpsocket.sendto(insurance, address)
            print 'Phase3: The cost estimation request from Patient2 with insurance plan', insurance, 'has been sent to the doctor with port number', udpport,'and IP address', udpsocket.getpeername()[0]

            cost,addr=udpsocket.recvfrom(2048)
            print 'Phase3: Patient2 receive $',cost, 'estimation cost from doctor with port number', udpport


            print 'Phase3: End of Phase3 for Patient2'

    else:
        clientsocket.close()

    clientsocket.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import socket

while True:
    serverport=42000
    serverhost='127.0.0.1'

    #create UDP socket
    serversocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    serversocket.bind((serverhost, serverport))
    print 'Phase3: Doctor2 has a static UDP port', serverport, 'and IP Address', serverhost

    name, addr = serversocket.recvfrom(2048)
    insurance, addr = serversocket.recvfrom(2048)
    print 'Phase3: Doctor2 receives the request from the patient with port number', addr[1], 'and name', name, 'with the insurance plan', insurance  
    
    #open doc1.txt check cost
    dic={}
    try:
        with open('input/doc2.txt', 'r') as f:
            for line in f.readlines():
                if not line:
                    continue
                line=line.split()
                k=line[0]
                v=line[1]
                dic[k]=v
            print dic
            f.close()
    except IOError:
        print 'File is not found'
        serversocket.close()
        sys.exit(1)
    
    #print repr(insurance)
    insurance = insurance.strip('\n')
    if (dic.has_key(insurance)):
        cost = dic.get(insurance)
        
        #match patient insurance in doc.txt
        serversocket.sendto(cost, addr)
        print 'Phase3: Doctor2 has sent estimated price $',cost, 'to patient with port number', addr[1]

    else:
        print 'Insurance plan is not match'
        break
        serversocket.close()
    

    
serversocket.close()

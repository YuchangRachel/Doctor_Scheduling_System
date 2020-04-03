#!/usr/bin/env python

import socket
import threading
import sys

udic={}  #global updated time index list

class ThreadServer(object):
    #define class member create serversocket
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #release port address guarantee port address can be reused
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    #listen incomming clients, build connection with multi clients via multithread
    #use the main thread just for listening for new clients. When one connects, the main thread creates a new thread that just listens to the new client and ends when it doesn't talk for 60 seconds.
    def listen(self):
        #connection queue maxnum
        self.sock.listen(2)
        #new client has new accept
        while True:
            conn, addr = self.sock.accept()
            conn.settimeout(60)
            t=threading.Thread(target=self.handle_client, args=(conn, addr))
            t.start()


    def handle_client(self, conn, addr):
        global udic
        try:
            msg=conn.recv(1024)
            list1=msg.split()
            if not msg:
                raise error('Client disconnected')
            print '---------------------------------------------\nPhase1:The Health Center Server has received request from a patient with username', list1[0], 'and password', list1[1]

            #load user database
            #open file users.txt and store infor in its memoery
            try:
                with open('input/users.txt', 'r') as f:
                    store=f.read()
                print 'User database:\n', store
            except IOError:
                print 'File is not found'
                conn.close()
                sys.exit(1)

            list2=store.split()

            dict={}
            dict[list2[0]]= list2[1]
            dict[list2[2]]= list2[3]

            if (dict.has_key(list1[0])):
                if (dict.get(list1[0]) == list1[1]):
                    response="Success"
                    conn.send(response)
                    print 'Phase1: The Health Center Server sends the response:', response, 'to patient with username', list1[0]

                    ask=conn.recv(1024)
                    print 'Phase2: The Health Center Server receives a request for available time slots from patients with port number:', conn.getpeername()[1], 'and IP Address:', conn.getpeername()[0] 

                    time=""
                    d={}
                    #communication only via string, not list
                    try:
                        f=open('input/availabilities.txt', 'r')
                        for l in f:
                            k,v = l.strip().split(' ', 1)
                            d[k]=v

                        if len(udic) == 0:
                            udic = d.copy()
                        keys=udic.keys()
                        keys.sort()
                        for k in keys:
                            ls = k + " " + udic[k]
                            print ls

                        for k in keys:
                            t = k + " " + " ".join(udic[k].split()[:2]) + '\n'
                            time += t
                        f.close()
                    except IOError:
                        print "File is not accessible"
                        conn.close()
                        sys.exit(1)
                        
                    
                    conn.send(time)
                    print 'Phase2: The Healther Center Server sends available time slots to patients with username',list1[0]
                    
                    while True:
                        choice=conn.recv(1024)
                        choicestr=choice.split(' ')
                        prefer=choicestr[1] + ""
                        
                        #check if prefer is included in indexlist or not, maybe not integer
                        ks=d.keys()
                        if prefer not in ks:
                            print 'Receiving invalid time index, let patient re-enter'
                            conn.send('Invalid')
                        else:
                            break

                    print 'Phase2: The Health Center Server receives a request for appoinment',prefer, 'from patient with port number:', conn.getpeername()[1], 'and username', list1[0]

                    if udic.has_key(prefer):
                        docInfor = udic[prefer].split()[-1] + " " 
                        conn.send(docInfor)
                        print 'Phase2: The Health Center Server confirms the following appointment', prefer, 'to patient with username', list1[0]
                        del udic[prefer]     #delete chosen choice
                    else:
                        conn.send('notavailable')
                        print 'Phase2: The Health Center Server rejects the following appoinment', prefer, 'to patient with username',list1[0]

                else:
                    response="Failure"
                    conn.send(response) 
                    print 'Phase1: The Health Center Server sends the response:', response, 'to patient with username', list1[0]
                    conn.close()
                
            else:
                response="Failure"
                conn.send(response)
                print 'Phase1: The Health Center Server sends the reponses:', response, 'to patient with username', list1[0]
                conn.close()
        except:
            conn.close()
        
        conn.close()
    #end of handle_client function


if __name__ == "__main__":
    serverPort=21000
    serverHost='127.0.0.1'
    print ("Phase1:The Health Center Server has port number: %s and IP address: %s " % (serverPort, serverHost))
    ThreadServer(serverHost, serverPort).listen()







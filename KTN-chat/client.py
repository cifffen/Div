'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
from threading import Thread
import json
import time
import sys

loginTimeOut = 5
SERVER = 'localhost'
PORT = 9999

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(2)

    def start(self, host, port):
        try:
            self.connection.connect((host, port))
        except:
            print "Can not connect to server.. Please try again later"
            terminate()

    def message_received(self, message, connection):
        if len(message) != 0:
            try:
                msg = json.loads(message)
                response = msg['response'] 
                if response == 'logout':
                    if 'error' in msg:
                        print "\n" + msg['username'] +" : " + msg['error']
                    else:
                        print "\n" + msg['username'] + " logged out"
                elif response == 'login':
                    if not 'error' in msg:
                        print "\n" + msg['username'] + " logged in"
                elif response == 'message':
                    if 'error' in msg:
                        print "\n"+msg['error']
                        self.loginRequest()
                        return
                    else:
                        print "\nMessage: " + msg['message']
            except:
                print "\nInvalid message received"
                return
            return
            
    def connection_closed(self):
        print "\nConnection with server is closed"
        terminate()
    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()
        #self.connection_closed(self.connection)
    
    def loginRequest(self):
        while 1:
            username = raw_input("\nType username: ")
            try:
                login = {'request': 'login', 'username': username}
                loginJson = json.dumps(login)
                test = json.loads(loginJson)
            except:
                print "\nInvalid username"
                continue
            try:
                self.send(loginJson)
                responseJson = self.connection.recv(1024).strip()
                time_start = time.time()
                while len(responseJson) == 0:
                    responseJson = self.connection.recv(1024).strip()
                    diff = int(time.time() - time_start)
                    if diff%60 >= loginTimeOut:
                        print "Timeout"
                        raise Exception()
                print responseJson
            except:
                print "\nNo contact with server"
                self.connection_closed()
            try:
                response = json.loads(responseJson)
                
            except:
                print "\nInvalid response from server"
                self.connection_closed()
            try:
                if 'error' in response:
                    if 'username' in response:
                        print response['username']
                    print response['error']
                    continue
                else:
                    print response['username'] + ' logged in, printing all messages: '
                    print response['messages']
                    break
            except:
                print "Invalid message received"
                self.connection_closed()
                
    def logoutRequest(self):
        print "Logging out.."
        logout = {'request': 'logout'}
        logoutJson = json.dumps(logout)
        self.send(logoutJson)
        self.force_disconnect()
        self.connection_closed()
            
    def sendMessage(self, data):
        try:
            decoded = data.decode("utf-8")
            msg = {'request': 'message', 'message': decoded}
            msgJson = json.dumps(msg)
        except:
            print "Invalid text"
            return
        try:
            self.send(msgJson)
        except:
            print "No contact when sending msg to server"
            self.connection_closed()

def terminate():
    print "Closing program.."
    sys.exit()                
            
if __name__ == "__main__":
    print "Welcome to The KTN-chat!"
    client = Client()
    client.start(SERVER, PORT)
    client.loginRequest()

    print "Type in a message followed by enter to send,"
    print "please type \'logout\' to log out"
    
    msgWorkerThread = ReceiveMessageWorker(client,client.connection)
    msgWorkerThread.start()
    while 1:
        msg = raw_input()
        if msg == 'logout':
            client.logoutRequest()    
        client.sendMessage(msg)
    msgWorkerThread.join()
    client.force_disconnect()
    print "Client disconnected"



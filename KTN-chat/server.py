'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer
import re
import json
import socket
import sys
'''

The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''
reload(sys) 
sys.setdefaultencoding('utf-8') 
class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	global onlineClients
            # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print('Client connected @' + self.ip + ':' + str(self.port))
        # Wait for data from the client
        while True:
            try:
                data = self.connection.recv(1024)
                # Check if the data exists
                # (recv could have returned due to a disconnect)
                if data:
                    self.requestHandler(data)
                    # Return the string in uppercase
                    # self.connection.sendall(data.upper())
                else:
                    print('Client disconnected!')
                    #handle disconnected client here instead?
                    break
            except socket.timeout:
                print 'Socket timeout'
                continue
            except:
                print('Lost connection to client!')
                connKey = self.checkIfLoggedIn()
                if connKey != '$NotInOnlineList$':
                    del onlineClients[connKey]
                break

    def requestHandler(self, data):
        dict1 = json.loads(data.decode("utf-8"))
        if 'request' in dict1:
            request = dict1['request']
            '''
if request in self.requestTypes:
print(request + ' is in requestTypes')
self.requestTypes[request](dict1)
'''
            if request == 'login':
                self.handleLoginRequest(dict1)
            elif request == 'message':
                self.handleMessageRequest(dict1)
            elif request == 'logout':
                self.handleLogoutRequest()
    def handleLoginRequest(self, dict1):
	global onlineClients
        global messages
        if 'username' in dict1:
            username = dict1['username']
            valUser = self.validUsername(username)
            if valUser == 1:
                data = json.dumps({'response': 'login', 'username': username, 'messages': messages})
		msg = json.dumps({'response': 'message','message': 'User '+username+' logged in.'})
                toLog = 'User ' + username +' logged in.' + '\n'
                messages += toLog
                for conn in onlineClients.values():
                    conn.sendall(msg.encode())
                onlineClients[username] = self.connection
            elif valUser == 0:
                data = json.dumps({'response': 'login', 'error': 'Invalid username!', 'username': username})
            else:
                data = json.dumps({'response': 'login', 'error': 'Name already taken!', 'username': username})
            self.connection.sendall(data.encode())
        return

    def handleMessageRequest(self, dict1):
	global onlineClients
        global messages
        if self.checkIfLoggedIn() != '$NotInOnlineList$':
            if 'message' in dict1:
		user = self.checkIfLoggedIn()
		msg = json.dumps({'response': 'message', 'message': user+': '+dict1['message']})
		toLog = user+': '+dict1['message'] + '\n'
                messages += toLog
                for conn in onlineClients.values():
                    conn.sendall(msg.encode())
        else:
            msg = json.dumps({'response': 'message', 'error': 'You are not logged in!'})
            self.connection.sendall(msg.encode())
    
    def checkIfLoggedIn(self):
	global onlineClients
        for k, v in onlineClients.items():
            if v:
                if self.connection == v:
                    return k
        return '$NotInOnlineList$'


    def handleLogoutRequest(self):
	global onlineClients
	global message
        user = self.checkIfLoggedIn()
        if user != '$NotInOnlineList$':
            msg = json.dumps({'response': 'logout', 'username': user+'1'})
	    print(onlineClients.keys())
	    print(msg)
	    self.connection.sendall(msg.encode())
            data = json.dumps({'response': 'message', 'message': 'User '+user+' logged out.\n'})
            toLog = 'User ' + username +' logged out.' + '\n'
            messages += toLog
            print(onlineClients.keys())
            for conn in onlineClients.values():
               conn.sendall(data.encode())
            del onlineClients[connKey]
        else:
            msg = json.dumps({'response': 'logout','error': 'Not logged in!', 'username': user+'\n'})
            self.connection.sendall(msg.encode())

    def validUsername(self, username):
	global onlineClients
        if re.match(r'\w+$', username,re.UNICODE):
            # valid username! see: http://docs.python.org/2/library/re.html#search-vs-match [ctrl] + f: When the LOCALE and UNICODE flags are not specified, matches any alphanumeric character and the underscore;
                if username not in onlineClients:
                    #username not taken, return true!
                    return 1
                else:
                    #username taken
                    return -1
        return 0 #username contains invalid characters
'''
requestTypes = { #Holds the different requests a client can send
'login' : handleLoginRequest(dict),
'message' : handleMessageRequest,
'logout' : handleLogoutRequest,
}

'''
'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


onlineClients = {}
messages = ""

if __name__ == "__main__":
    HOST = ''#78.91.29.196'
    PORT = 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


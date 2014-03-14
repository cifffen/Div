'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer
import re
import json
#from MessageWorker import ReceiveMessageWorker
'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''

class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
            # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print('Client connected @' + self.ip + ':' + str(self.port))
        # Wait for data from the client
        while True:
            print('Waiting for data')
            data = self.connection.recv(1024)
            # Check if the data exists
            # (recv could have returned due to a disconnect)
            if data:
                print(data.decode("utf-8"))
                self.requestHandler(data)
                # print data
                # Return the string in uppercase
                # self.connection.sendall(data.upper())
            else:
                print('Client disconnected!')
                break

    def requestHandler(self, data):
        #try:
        dict1 = json.loads(data.decode("utf-8"))
        #print(dict1)
        if 'request' in dict1:
            request = dict1['request']
            #print('Request: ' + request)
            '''
            if request in self.requestTypes:
                print(request + ' is in requestTypes')
                self.requestTypes[request](dict1)
            '''
            if request == 'login':
                #if 'username' in dict1.keys():
                print("login!")
                #    print(dict1['username'])
                self.handleLoginRequest(dict1)
            elif request == 'message':
                print("New message!")
                self.handleMessageRequest(dict1)
            elif request == 'logout':
                print("logout!")
                self.handleLogoutRequest()

        #except: 
            #data = json.dumps({'response': 'login', 'error': 'Something is wrong!', 'username': 'jau'})
            #self.connection.sendall(data)
         #   print('Invalid request')
            
    def handleLoginRequest(self, dict1):
        #print(dict1)
        if 'username' in dict1:
            print('username: ' + dict1['username'])
            username = dict1['username']
            valUser = self.validUsername(username)
            print("Valuser = ", valUser)
            if valUser == 1:
                data = json.dumps({'response': 'login', 'username': username, 'messages': 'ingenting'})
                print("add client!")  
                onlineClients[username] = self.connection
                print(onlineClients.keys())
            elif valUser == 0:
                data = json.dumps({'response': 'login', 'error': 'Invalid username!', 'username': username})
            else:
                data = json.dumps({'response': 'login', 'error': 'Name already taken!', 'username': username})
            self.connection.sendall(data.encode())
            print("send!")
        return

    def handleMessageRequest(self, dict1):
        if self.checkIfLoggedIn() != '$NotInOnlineList$':
            #print("Logged in!")
            if 'message' in dict1:
                print("Message is:")
                msg = json.dumps({'response': 'message', 'message': dict1['message']})
                print(msg)
                for conn in onlineClients.values():
                    conn.sendall(msg.encode())
        else:
            msg = json.dumps({'response': 'message', 'error': 'You are not logged in!'})
            self.connection.sendall(msg.encode())
        
    def checkIfLoggedIn(self):
        for k, v in onlineClients.items():
            if v:
                if self.connection == v:
                    return k
        return '$NotInOnlineList$'

    def handleLogoutRequest(self):
        user = self.checkIfLoggedIn()
        if user != '$NotInOnlineList$':
            msg = json.dumps({'response': 'logout', 'username': user})
            del onlineClients[user]
            print('User ' + user + ' deleted!')
            print(onlineClients.keys())
        else:
            msg = json.dumps({'response': 'logout','error': 'Not logged in!', 'username': user})
        self.connection.sendall(msg.encode())


    def validUsername(self, username):
        if re.match(r'\w+$', username):
            # valid username! see: http://docs.python.org/2/library/re.html#search-vs-match [ctrl] + f: When the LOCALE and UNICODE flags are not specified, matches any alphanumeric character and the underscore;
                if username not in onlineClients:
                    #username not taken, return true!
                    return 1
                else:
                    #username taken
                    return -1
        return 0 #username contains invalid characters
'''
    requestTypes = {    #Holds the different requests a client can send
        'login'     : handleLoginRequest(dict),
        'message'   : handleMessageRequest,
        'logout'    : handleLogoutRequest,
     }

'''
'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


onlineClients = {}

if __name__ == "__main__":
    HOST = ''#78.91.29.196'
    PORT = 9999


    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()






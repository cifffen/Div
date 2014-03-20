'''
KTN-project 2013 / 2014
Python daemon thread class for listening for events on
a socket and notifying a listener of new messages or
if the connection breaks.

A python thread object is started by calling the start()
method on the class. in order to make the thread do any
useful work, you have to override the run() method from
the Thread superclass. NB! DO NOT call the run() method
directly, this will cause the thread to block and suspend the
entire calling process' stack until the run() is finished.
it is the start() method that is responsible for actually
executing the run() method in a new thread.
'''

'''
Look here for more threading info:
http://www.radekdostal.com/content/android-bluetooth-chat-multi-thread-echo-server-python
http://stackoverflow.com/questions/2915160/how-do-i-abort-a-socket-recv-from-another-thread-in-python
'''

from threading import Thread
import time
import socket

class ReceiveMessageWorker(Thread):

    def __init__(self, listener, connection):
    	Thread.__init__(self)
    	self.daemon = True
    	self.connection = connection
    	self.listener = listener
        

    def run(self):
    	while 1:
            try:
                data = self.connection.recv(1024).strip()
                if len(data) != 0:
                    self.listener.message_received(data, self.connection)
            except socket.timeout:
                continue
            except:
                #print "Socket Error"
                print "\nDisconnected from messageworker"
                self.listener.connection_closed()
                break
                        

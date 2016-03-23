import sys
import socket
import threading
import authenticateUser
import handleMessage as hm
import os

userpass = authenticateUser.impUsers()
activeClients = {}
BLOCKTIME = os.environ['BLOCK_TIME']


class ChatServer(object):
		    try:
					        def __init__(self, host, port):
									            self.host = host
												            self.port = port
															            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
																		            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
																					            self.sock.bind((self.host, self.port))

																								        def listen(self):
																												            self.sock.listen(5)
																															            print "Serving on port %s" %port
																																		            while True:
																																							                client, address = self.sock.accept()
																																											                blocked = authenticateUser.checkBlocked(address,BLOCKTIME)
																																															                if blocked == True:
																																																					                    client.send("Blocked")
																																																										                    client.close()
																																																															                    continue
																																																																		                else:
																																																																								                    client.send("continue")
																																																																													                print "Client %s connected at address %s"%(client, address)
																																																																																	                threading.Thread(target = self.clientThread,args = (client,address)).start()


																																																																																					        def clientThread(self, client, address):
																																																																																									            accept = authenticateUser.login(client, userpass, activeClients)
																																																																																												            if accept[0] == True:
																																																																																																	                activeClients[accept[1]] = client
																																																																																																					            else:
																																																																																																										                if accept[1] == "logout" :
																																																																																																																                    return 0
																																																																																																																			                if accept[1] == "Block":
																																																																																																																									                    authenticateUser.block(address)
																																																																																																																														                    client.send("Too many attempts. Closing Connection")
																																																																																																																																			                    client.close()
																																																																																																																																								            while True:
																																																																																																																																													                try:
																																																																																																																																																			                    data = client.recv(1024) + "\n"
																																																																																																																																																								                    print data
																																																																																																																																																													                except:
																																																																																																																																																																			                    print "Client Log Off"
																																																																																																																																																																								                    return 0
																																																																																																																																																																											                if data:
																																																																																																																																																																																	                    hm.handle(client, data, activeClients)
																																																																																																																																																																																						    except KeyboardInterrupt:
																																																																																																																																																																																									        print 'Goodbye\n'
																																																																																																																																																																																											        try:
																																																																																																																																																																																															            sys.exit(0)
																																																																																																																																																																																																		        except SystemExit:
																																																																																																																																																																																																						            os._exit(0)

																																																																																																																																																																																																									if __name__ == "__main__":
																																																																																																																																																																																																											    try:
																																																																																																																																																																																																														        port = int(sys.argv[1])
																																																																																																																																																																																																																        ChatServer('',port).listen()
																																																																																																																																																																																																																		    except KeyboardInterrupt:
																																																																																																																																																																																																																					        print '\n Goodbye!'
																																																																																																																																																																																																																							        try:
																																																																																																																																																																																																																											            sys.exit(0)
																																																																																																																																																																																																																														        except SystemExit:
																																																																																																																																																																																																																																		            os._exit(0)

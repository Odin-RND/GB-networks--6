#!/bin/python3
import socket
import threading
from datetime import datetime

#get white IP address from socketname with test connection
testsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
testsock.connect(("8.8.8.8",80))
# Connection Data
host = testsock.getsockname()[0]
testsock.close()
port = int(input('Service port number: '))

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
#clients = {}
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        #clients[client] = nickname
        content = (str(datetime.now())+':'+str(nickname)+':'+str(client)+'\n')
        log = open('server.log','a')
        log.write(content)
        log.close()

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening on IP {} and port {}".format(host,port))
receive()

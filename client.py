import socket
import threading
import sys

# Choosing Nickname
nickname = input("Choose your nickname: ")
port = int(input("Enter service's remote port number: "))

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('193.124.112.54', port))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        text = input('')
        if text == '\EXIT':
            client.send(text.encode('utf-8'))
        else:
            message = '{}: {}'.format(nickname, text)
            client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
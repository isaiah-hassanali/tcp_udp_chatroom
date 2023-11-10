# Assignment: TCP Simple Chat Room - TCP Client Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need sys, socket, argparse, select, threading (or _thread) libraries for the client implementation.
#    Feel free to use any libraries as well.
import argparse
import socket
import sys
from threading import Thread

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the client side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts,and client shutdown.
def run(clientSocket: socket.socket, clientname: str):
    try:
        clientSocket.send(clientname.encode())

        # run in a thread to send messages
        def send_messages():
            while True:
                message = input(f"{clientname}: ")
                if not message:
                    print("\033[F\033[K", end="") # to keep the terminal output clean
                else:
                    message = f"MESSAGE\r\n\r\n{clientname}\r\n{message}"
                    clientSocket.send(message.encode())

        # run in a thread to receive messages
        def receive_messages():
            while True:
                message = clientSocket.recv(2048)
                print("\r\x1b[K", end="")
                print(message.decode())
                print(f"{clientname}: ", end="")
                sys.stdout.flush()

        receive_thread = Thread(target=receive_messages, daemon=True)
        receive_thread.start()
        send_thread = Thread(target=send_messages, daemon=True)
        send_thread.start()

        while True:
            pass

    except KeyboardInterrupt:
        print("\nDisconnecting.")
        message = "QUIT\r\n\r\n" + clientname
        clientSocket.send(message.encode())
        exit(0)

# **Main Code**:  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python tcp_client.py username
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    client_socket.connect((server_addr, server_port))

    run(client_socket, client_name)
 

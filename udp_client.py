# Assignment: UDP Simple Chat Room - UDP Client Code Implementation

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
def run(clientSocket: socket.socket, clientname: str, serverAddr: str, serverPort: int):
    try:
        print("Connecting to server. Hit CTRL-C to quit.")
        connection_string = "JOIN\r\n\r\n" + clientname
        clientSocket.sendto(connection_string.encode(), (serverAddr, serverPort))

        def send_messages():
            while True:
                message = input(f"{clientname}: ")
                if not message:
                    print("\033[F\033[K", end="") # to clean terminal output
                else:
                    message = f"MESSAGE\r\n\r\n{clientname}\r\n{message}"
                    clientSocket.sendto(message.encode(), (serverAddr, serverPort))

        def receive_messages():
            while True:
                message, _ = clientSocket.recvfrom(2048)
                print("\r\x1b[K", end="") # to clean terminal output
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
        clientSocket.sendto(message.encode(), (serverAddr, serverPort))
        exit(0)

# **Main Code**:  
if __name__ == "__main__":
    
    # Arguments: name address
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')  # to use: python udp_client.py username
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    run(clientSocket, clientname, serverAddr, serverPort)  # Calling the function to start the client.

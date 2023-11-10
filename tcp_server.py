# Assignment: TCP Simple Chat Room - TCP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, threading, select, time libraries for the client.
#    Feel free to use any libraries as well.
import socket
from threading import Thread

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
def run(serverSocket: socket.socket, serverPort: int):
    try:
        print("Server is running...")

        # this function handles a single client
        def handle_client(client_socket: socket.socket, client_address: tuple[str, int]):
            # first received message is their username
            data = client_socket.recv(1024)
            print(f"User {data.decode()} {client_address} has joined.")

            # continually receive data
            while True:
                data = client_socket.recv(1024)

                # forceful disconnection
                if not data:
                    print(f"The client at {client_address} disconnected.")
                    clients.remove((client_socket, client_address))
                    client_socket.close()
                    break
                
                else:
                    request, payload = data.decode().split("\r\n\r\n")

                    # broadcast a message to all connected clients
                    if request == "MESSAGE":
                        username, content = payload.split("\r\n")
                        print(f"Message received from {username} {client_address}: {content}")
                        message = f"{username}: {content}"
                        for client in clients:
                            if client[1] != client_address:
                                client[0].send(message.encode())

                    # graceful disconnection
                    elif request == "QUIT":
                        print(f"{payload} {client_address} has disconnected.")
                        client_socket.close()
                        clients.remove((client_socket, client_address))
                        break
        # accept clients and create threads to handle them
        while True:
            client_socket, client_address = server_socket.accept()
            clients.append((client_socket, client_address))
            client_handler = Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_handler.start()

    # shutdown the server
    except KeyboardInterrupt:
        print("\nShutting down.")
        serverSocket.close()
        exit(0)


# **Main Code**:  
if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creating a TCP socket.
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3) # size of the waiting_queue that stores the incoming requests to connect.
    
    # please note that listen() method is NOT for setting the maximum clients to connect to server.
    # didnt get it? basically, when the process (assume process is man that execute the code line by line) is executing the accept() method on the server side, 
    # the process holds or waits there until a client sends a request to connect and then the process continue executing the rest of the code.
    # good! what if there is another client wants to connect and the process on the server side isnt executing the accept() method at the same time,
    # Now listen() method joins the party to solve this issue, it lets the incoming requests from the other clients to be stored in a queue or list until the process execute the accept() method.
    # the size of the queue is set using listen(size). IF YOU STILL DONT GET IT, SEND ME AN EMAIL.

    clients: list[tuple[socket.socket, tuple[str, int]]] = [] #list to add the connected client sockets , feel free to adjust it to other place
    run(server_socket,server_port)# Calling the function to start the server.

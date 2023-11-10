# Assignment: UDP Simple Chat Room - UDP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, select, time libraries for the client.
#    Feel free to use any libraries as well.
import socket

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
def run(serverSocket: socket.socket, serverPort: int):
    try:
        serverSocket.bind(("", serverPort))
        print("Server is running...")

        clients: set[tuple[str, int]] = set()
        
        while True:
            data, sender_address = serverSocket.recvfrom(2048)
            request, payload = data.decode().split("\r\n\r\n")

            if request == "JOIN":
                clients.add(sender_address)
                print(f"User {payload} {sender_address} has joined.")

            elif request == "MESSAGE":
                username, content = payload.split("\r\n")
                print(f"Message received from {username} {sender_address}: {content}")
                message = f"{username}: {content}"
                for client_address in clients:
                    if client_address != sender_address:
                        serverSocket.sendto(message.encode(), client_address)

            elif request == "QUIT":
                print(f"{payload} {sender_address} has disconnected.")
                clients.remove(sender_address)

    except KeyboardInterrupt:
        print("\nShutting down.")
        serverSocket.close()
        exit(0)

# **Main Code**:  
if __name__ == "__main__":
    
    serverPort = 9301  # Set the `serverPort` to the desired port number (e.g., 9301).
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.
    run(serverSocket, serverPort)  # Calling the function to start the server.

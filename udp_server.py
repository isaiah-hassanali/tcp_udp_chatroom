# Assignment: UDP Simple Chat Room - UDP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, select, time libraries for the client.
#    Feel free to use any libraries as well.

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
def run(serverSocket, serverPort):
    # The main server function.
    pass

# **Main Code**:  
if __name__ == "__main__":
    
    serverPort = 9301  # Set the `serverPort` to the desired port number (e.g., 9301).
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.
    run(serverSocket, serverPort)  # Calling the function to start the server.

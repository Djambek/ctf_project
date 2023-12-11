import socket
HOST = socket.gethostname()
PORT = 5001
server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((HOST, PORT))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(8)

def check_user_input(conn, args, message_error):
    while 1:
        user_input = conn.recv(1024).decode()
        for obj in args:
            if user_input == obj[0]:
                return obj[1](*obj[2:])
        conn.send(message_error.encode())
                

def say_hello(conn):
    data = "Hi, u visit a note saver) If u have had already account enter 1, else 2\r\nInput: "
    conn.send(data.encode())
    return check_user_input(conn, [["1\n", sign_in, conn], ["2\n", register, conn]], "Your input is invalid, try again!\r\nInput: ")
            
          

def sign_in(conn):
    data = "Please enter your token. If you want go back enter q\r\nInput:"
    conn.send(data.encode())
    conn.close()
def register(conn):
    data = "You most copy and save your token, if you lose it your notes will be deleted!"
    conn.send(data.encode())
    conn.close()
while True:
    conn, address = server_socket.accept()  # accept new connection
    say_hello(conn)

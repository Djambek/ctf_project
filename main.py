import socket
from threading import Thread 
from db import *
import random, string

HOST = socket.gethostname()
PORT = 5002
server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((HOST, PORT))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(8)

def print_board(conn):
    conn.send("\r\n---------------------------------\r\n".encode())


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
    print_board(conn)
    data = "Please enter your token. If you want go back enter q\r\nInput: "
    conn.send(data.encode())
    while 1:
        user_input = conn.recv(1024).decode().replace("\n", "")
        if user_input == 'q':
            return say_hello(conn)
        elif check_token(user_input):
            return main_page(conn, user_input)
        
        conn.send("Token is invalid or you didn't create notes and token removed. Enter your token, if you want go back enter q\r\nInput: ".encode())

def main_page(conn, token):
    print_board(conn)
    data = "Что вы хотите делать?\r\n\n1) Вывести все заметки\r\n2) Создать новую заметку\r\nНажмите q если хотите вернуться!\r\nВвод: "
    conn.send(data.encode())
    return check_user_input(conn, [["1\n", all_notes, conn, token], ["2\n", create_new_note, conn, token], ['q\n', sign_in, conn]], "Неверный ввод, подумайте и введите снова\r\nВвод: ")

def all_notes(conn, token):
    print_board(conn)
    print(get_files(token))
    els = get_files(token)
    data = "Ваши заметки:\r\n"
    for ind, el in enumerate(els):
        data += f"\t{ind+1})" + el[0]+"\r\n"
    data += "Введите номер заметки, чтобы ее посмотреть, если хотите назад, то введите q\r\nВвод: "
    conn.send(data.encode())
    conn.close()

def view_note(conn, path):
    print_board(conn)
    data = open(path, "r").read()
    
    
def create_new_note(conn, token):
    print_board(conn)
    conn.send("Push your wish in your ass")
    conn.close()

def generate_token(lenght):
    lett = string.ascii_lowercase + string.ascii_uppercase + "1234567890!@#$%^&*()"
    return "".join(random.choice(lett) for i in range(lenght))

def register(conn):
    print_board(conn)
    token = generate_token(64)
    data = f"You most copy and save your token, if you lose it your notes will be deleted!\r\nВаш токен: {token}"
    conn.send(data.encode())
    return main_page(conn, token)


while True:
    conn, address = server_socket.accept()  # accept new connection
    t = Thread(target=say_hello, args=(conn,))
    t.start()
    # thread.start_new_thread(say_hello, (conn,))
    
server_socket.close()






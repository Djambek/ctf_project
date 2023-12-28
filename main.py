import socket
from threading import Thread 
from db import *
import random, string
import os
from hashlib import sha256

HOST = socket.gethostname()
PORT = 5001
DIR = "notes/"
server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((HOST, PORT))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(8)

def hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

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
    vars = [["q\n", main_page, conn, token]]
    if len(els) == 0:
        conn.send("У вас нет заметок! Чтобы вернуться назад нажмите q\r\nВвод: ".encode())
    else:
        for ind, el in enumerate(els):
            data += f"\t{ind+1})" + el[0]+"\r\n"
            vars.append([f"{ind+1}\n", get_note_text, conn, el[1], el[2], token])
        data += "Введите номер заметки, чтобы ее посмотреть, если хотите назад, то введите q\r\nВвод: "
        conn.send(data.encode())
    return check_user_input(conn, vars, "Неверный ввод, подумайте и введите снова\r\nВвод: ")

def get_note_text(conn, path, id, token):
    print_board(conn)
    try:
        file = open(path, 'r').read()
        conn.send(file.encode())
        conn.send("Введите d, если хотите удалить, введите q, чтобы вернуться назад\r\nВвод: ".encode())
        return check_user_input(conn, [['d\n', delete_note, conn, id, path, token], ['q\n', all_notes, conn, token]], "Неверный ввод, подумайте и введите снова\r\nВвод: ")
    except:
        conn.send("Произошла ошибка, такое тоже бывает)".encode())
        conn.close()

def delete_note(conn, id, path, token):
    print("Id to delete: ", id)
    delete_note_db(id)
    os.remove(path)
    return all_notes(conn, token)

    
def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def create_new_note(conn, token):
    print_board(conn)
    conn.send("Введите заголовок для заметки, нажмите enter, чтобы его ввести. Нельзя использовать символы переноса строки) Ввод: ".encode())
    header = conn.recv(1024).decode().replace('\n', '')
    conn.send("Введите текст для заметки, нажмите enter, чтобы его ввести.Нельзя использовать символы переноса строки)\nВвод: ".encode())
    body = recvall(conn).decode()
    path = f"{DIR + hash(header)}.txt"
    with open(path,  'w') as f:
        f.write(body)
    create_new_file(header, path, token)
    conn.send("Заметка сохранена".encode())
    return main_page(conn, token)


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






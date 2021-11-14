import sys
from socket import socket, AF_INET, SOCK_STREAM
import json
from Utils.Cipher import Cipher
from Utils.Config import Config

HOST = 'localhost'
PORT = 4000
SIZE = 1024

def initialize_connection():
  sock = socket(AF_INET, SOCK_STREAM)
  sock.bind((HOST, PORT))
  print(f'Wainting for connection on port {PORT}')
  sock.listen(1)
  
  while True:
    connection, _ = sock.accept()
    try:
      connection.sendall(json.dumps({
        'status': 'initialize',
      }).encode())

      data = json.loads(connection.recv(SIZE).decode())

      if 'status' in data and data['status'] == 'connected':
        return connection
    except Exception:
      print("Couldn't connect. Wainting another connection")


def connect():
  sock = socket(AF_INET, SOCK_STREAM)
  print(f'Connecting to port {PORT}')
  sock.connect((HOST, PORT))
  
  try:
    data = json.loads(sock.recv(SIZE).decode())

    if 'status' in data and data['status'] == 'initialize':
      sock.sendall(json.dumps({'status': 'connected'}).encode())

      print('Connected')
      return sock

  except Exception:
    print('Connection failed')
    exit()


def send_message(connection, cipher):
  plain_text = input('Message: ')
  if plain_text == 'q':
    print('Sending exit status')

    connection.sendall(json.dumps({'status': 'exit'}).encode())
    connection.close()

    return False
  else:
    connection.sendall(
      json.dumps({
        'offset': cipher.get_offset(),
        'cipher': list(cipher.encrypt(plain_text, cipher.get_offset()))
      }).encode()
    )
  return True


def receive_message(connection, cipher):
  data = json.loads(connection.recv(SIZE).decode())

  if 'status' in data and data['status'] == 'exit':
    print('Exiting')
    connection.close()
    exit()

  if 'offset' not in data or 'cipher' not in data:
    return 'Invalid message received.'

  msg_offset = data['offset']
  cipher_text = data['cipher']
  return cipher.decrypt(cipher_text, int(msg_offset)).decode()


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Bad usage. Usage: python peer.py 1/2')
    exit()

  config = Config()
  cipher = Cipher(config.get_generator(), config.get_key())
  
  connection = None

  if sys.argv[1] == '1':
    connection = initialize_connection()

  elif sys.argv[1] == '2':
    connection = connect()
    msg = receive_message(connection, cipher)
    print('Received a message: ')
    print(msg)

  else:
    print(f'Bad usage. Usage: python peer.py 1/2')
    exit()

  while send_message(connection, cipher):
    msg = receive_message(connection, cipher)
    print('Received a message: ')
    print(msg)
    
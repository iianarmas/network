import socket
import argparse

parser = argparse.ArgumentParser(description='This is the client for the multi-threaded socket server.')

parser.add_argument('--host', metavar='host', type=str, nargs='?', default = socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)

args = parser.parse_args()

print(f'Connecting to server: {args.host} on port {args.port}')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((args.host, args.port))
    except Exception as err:
        raise SystemExit(f'We have failed to connect to host {args.host} on port {args.port}, because {err}')


    while True:
        msg = input('What do we want to send to the server?: ')
        s.sendall(msg.encode('utf-8'))
        if msg == 'exit':
            print('Client is saying goodbye')
            break

        data = s.recv(1024)
        print(f'Server response was: {data.decode()}')


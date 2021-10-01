import socket
import argparse
import threading

parser = argparse.ArgumentParser(description='This is the server for the multi-threaded socket server.')

parser.add_argument('--host', metavar='host', type=str, nargs='?', default = socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)

args = parser.parse_args()

print(f'Running the server on: {args.host} and port {args.port}')

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((args.host, args.port))
    s.listen(5)
except Exception as err:
    raise SystemExit(f'We could not bind the server on host: {args.host} to port {args.port} because {err}')


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f'New connection was made from IP: {ip}, on port {port}')

    while True:
        msg = client.recv(1024)
        if msg.decode() == 'exit':
            break
        print(f'Client said: {msg.decode()}')

        reply = f'You told me: {msg.decode()}'

        client.sendall(reply.encode('utf-8'))

    print(f'The client form IP: {ip}, and on port {port} has disconnected.')


    client.close()

# threading
while True:
    try:
        client, ip = s.accept()
        threading._start_new_thread(on_new_client, (client, ip))

    except KeyboardInterrupt:
        print('Shutting down the server.')
        break
    except Exception as err:
        print(f'Sorry, there is an error: {err}')

s.close()

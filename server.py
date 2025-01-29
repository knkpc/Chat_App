import socket




#Main server Function.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.5", 9091)) # local host should be added
server.listen()
print("server listening on port 9091")

while True:
    client_socket, addr = server.accept()
    print(f"Connection established with {addr}")
    data = client_socket.recv(1024)
    print(data.decode())
    client_socket.sendall(data)

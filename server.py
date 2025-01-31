import socket
import pickle
import uuid

my_client_details = []
client_details = {}

###checking the user existance
def user_exists(name,mobile):
    for user in my_client_details:
        if data["regname"] in user.values() and data["regphone"] in user.values():
            return True
    return False

#Main server Function.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9090)) # local host should be added
server.listen()
print("server listening on port 9090")

for i in range(1):
    
    client_socket, addr = server.accept()
    print(f"Connection established with {addr}")
    data = pickle.loads(client_socket.recv(1024))
    print(f" client host number and details {data}")

    # print(user_exists(data["regname"], data["regphone"]))

    if((user_exists(data, my_client_details)) == False):
        # Generating the Unique_id
        unique_id = str(uuid.uuid4())
        data["unique_id"] = unique_id
        client_details = dict(data) # shallow copy
    else:
        pass
    

    #client_details = {key:value for key,value in pickle.loads(data).items()}  #--> dictionary comprehension ( It is shallow copy) -> It is working
    #print(f"These are the stored Client details:-\n {client_details}")
   
    client_socket.sendall(pickle.dumps(unique_id))
    
    my_client_details.append(client_details)
    print(f"These are the stored MY Client details:-\n {my_client_details} \n")

    

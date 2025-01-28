import socket
import pickle
import time
import yaml

class usr_Reg:
    userName : str = None
    userPhone: str ="0000000000"
    userUUID: str =None

    def __init__(self, name:str,phone:str):
        self.userName=name
        self.userPhone=phone
        self.userUUID=self.getUUID(name,phone)

    def getUUID(self,name:str, phone:str):
        uuid=None
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        IP = "127.0.0.1"
        port = 9090
        newuser= dict(req ="Register",regname=name, regphone=phone)
        for i in range(5):
            try:
                s.connect((IP,port))
                s.sendall(pickle.dumps(newuser))
                uuid =pickle.loads(s.recv(1024))
                if uuid:
                    print(f"Registration successful")
                    break
            except Exception as e :
                print(f"{i+1}/5 :User Regestration Failure: reason {e}")
                time.sleep(1)

        return uuid


     


    
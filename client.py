import socket
import pickle
import sys
import time
import yaml

from concheck import configChk

class usr_Reg:
    userName : str = None
    userPhone: str =None
    userUUID: str =None

    def newusr(self, name:str,phone:str):
        print(f"newusr: name: {name} , phone: {phone}")
        self.userName=name
        if self.checkPhone(phone):
            
            self.userPhone=phone
        else:
            print(f"newusr: phone check failure")
            return False
        self.userUUID=self.getUUID(name,phone)
        if self.userUUID != None:
            configChk.createusr(dict(name=self.userName, phone=self.userPhone,UUID=self.userUUID))
        else:
            print(f"newusr: UUID Failed")
            return False
        return True
            
    

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
    
    def checkPhone(self,phone:str):
        """Check if the phone number is valid or not
         - should have 10 digits
         - should contain all digits
        """
        if len(phone) ==10:
            for d in phone:
                if not d.isdigit():
                    return False
        else:
            return False
        return True


class clientmain:

    def main():
        pass

    def loader():
        # for i in range(100):
        #     print("=",end="")
        configChk.checkusr()
        for i in range(10):
            sys.stdout.write("/ loading user details.." if i % 2 == 0 else "\\")  # Print / or \
            sys.stdout.flush()  # Ensure it is written immediately
            time.sleep(0.2)  # Wait for a brief moment before switching
            sys.stdout.write("\r")  # Return cursor to the start of the line

        # Add a final print to make sure the cursor is on a new line after finishing
        print()

    def userdetails():
        return configChk.readusr()
    
    def validUSR():
        """This checks for user file and validates user data in the file
            return:
            - 1 user details are valid
            - -1 user file doesn't exist
            - -2 username doesn't exist
            - -3 phone doesn't exist
            - -4 UUID doesn't exist 

        
        """
        if configChk.checkusr():
            data=configChk.readusr()
            count =-1
            for key,value in data.items():
                #print(f"{key}:{value}")
                count-=1
                if value is None:
                    return count
        else:
            return -1
        return 1
                    

    def loadusr():
        if clientmain.validUSR() ==1:
            
            return(clientmain.userdetails())
        else:
            print("New User")
            return(clientmain.Register())
        
    def Register():
        choice = input("do you want to Register? yes no")
        if choice=="yes" or "y" or "Yes":
            username = input("your name: ")
            phone = input("your phone:")

            while not usr_Reg().checkPhone(phone):
                phone = input("Enter Valid phone")

            nusr= usr_Reg().newusr(username,phone)
            if nusr:
                return "Registered"
            else:
                return "Registration Failed, please try again later"
        else:
            print("You need to register to continue..")






clientmain.loader()
print(clientmain.loadusr())


    
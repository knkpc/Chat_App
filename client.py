import socket
import pickle
import sys
import time


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

class Msg:
    to:str
    from_:str
    msg:str
    timestamp:float
    UUID:str
    Name:str
    Phone:str

    def __init__(self, to:str, UUID:str,Name:str,Phone:str):
        self.to=to
        self.from_=Name
        self.UUID=UUID
        self.Phone=Phone
    
    def sendmessage(self,msg:str):
        packet=dict(Request="msg",to=self.to,from_=self.Phone,UUID=self.UUID,message=msg,timestamp=time.time())
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        IP="127.0.0.1"
        port=9090
        for i in range(3):
            try:
                s.connect((IP,port))
                s.sendall(pickle.dumps(packet))
                response=pickle.loads(s.recv(1024))
                if response:
                    print("Message sent")
                    return True
                    
            except Exception as e:
                print(f"{i+1}/3 : Message delivery failure reason {e}")
                time.sleep(1)
        return False

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
    
    # # def validUSR():
    #     """This checks for user file and validates user data in the file
    #         return:
    #         - 1 user details are valid
    #         - -1 user file doesn't exist
    #         - -2 username doesn't exist
    #         - -3 phone doesn't exist
    #         - -4 UUID doesn't exist 

        
    #     """
    #     if configChk.checkusr():
    #         data=configChk.readusr()
    #         count =-1
    #         for key,value in data.items():
    #             #print(f"{key}:{value}")
    #             count-=1
    #             if value is None or value is "":
    #                 return count
    #     else:
    #         return -1
    #     return 1
    
    def validUSR():
        """This checks for user file and validates user data in the file
        
        Returns:
            - 1  : User details are valid
            - -1 : User file doesn't exist
            - -2 : Username is missing
            - -3 : Phone number is missing
            - -4 : UUID is missing
        """
        if not configChk.checkusr():
            return -1  # File doesn't exist

        data = configChk.readusr()

        # Ensure all required keys exist in the file
        required_keys = ["UUID", "name", "phone"]
        for key in required_keys:
            if key not in data:
                return -1  # File exists but missing required keys (invalid format)

        if not data["name"]:
            return -2
        if not data["phone"]:
            return -3
        if not data["UUID"]:
            return -4

        return 1  # All details are valid
           

    def loadusr():
        if clientmain.validUSR() ==1:
            
            return(clientmain.userdetails())
        else:
            print("New User")
            return(clientmain.Register())
        
    def Register():
        choice = input("do you want to Register? yes : no > ")
        while choice not in ["No","NO","n","N","yes", "y", "YES","Yes","Y"]:
            choice = input("Enter only yes : no > ")
        
        if choice in ["yes", "y","Y", "YES","Yes"]:
            username = input("your name: ")
            phone = input("your phone: ")

            while not usr_Reg().checkPhone(phone):
                phone = input("Enter Valid phone: ")

            nusr= usr_Reg().newusr(username,phone)
            if nusr:
                return "Registered"
            else:
                return "Registration Failed, please try again later"
        else:
            print("You need to register to continue..")



def display():
    options:list=[" 1. Show contacts",
                  " 2. Add contacts",
                  " 3. Search contacts",
                  " 4. Send Message",
                  "-1. Exit"]
    for option in options:
        print("\t \t",option)

def display_contacts():
    contacts=configChk.readcontacts()
    #print(f"in dispaly_contacts{contacts}")
    for usr,phone in contacts.items():
        print(f"{usr} = {phone}")

def add_contact(name:str, phone:str):
    configChk.addcontact(name,phone)
    return True

def get_condetails(name:str):
    contacts= configChk.readcontacts()
    if name in contacts:
        return contacts[name]
    else:
        return False

def message(x:Msg, to):
    print(f"Sending message to {to} : {x.to} ")
    print(f"\t \t !!!!!Enter Exit to stop sennding message and return to menu")
    message=""
    while message not in["Exit","exit"]:
        message= input('Enter message : ').strip()
        if len(message)>0 and message not in["Exit","exit"]:
            x.sendmessage(message)



clientmain.loader()
data=clientmain.loadusr()
print(f"\t \t \t Welcome to chat APP: {data['name']}")
choice=0
while True:
    try:
        display()
        choice = int(input('\t Enter you choice: ').strip())
        
        match choice:
            case 1:
                display_contacts()
            case 2:
                name:str =input('Enter name of contact: ').strip()
                phone:str=input('Enter contact numer: ').strip()
                while not usr_Reg().checkPhone(phone):
                    phone = input("Enter Valid phone: ").strip()
                if add_contact(name,phone):
                    print("contact added successfully")
                else:
                    print("Contact hasn't saved")
            
            case 3: 
                to:str =input('Enter name to search contact: ').strip()
                phone=get_condetails(to)
                if phone!=False:
                    print(f"Contact info: \n name: {to}\n Phone: {phone}")
                    
                else:
                    print(f"Unable to find contact {to} ")
            case 4:
                to:str =input('Enter contact name to send message: ').strip()
                phone=get_condetails(to)
                if phone!=False:
                    x= Msg(phone,data['UUID'],data['name'],data['phone'])
                    message(x,to)
                else:
                    print(f"Unable to find contact {to} \n add user in your contacts to send message")
            case -1:
                print('Exiting Application ;)')
                break
            
            case _:
                print('Invalid choice')
    except ValueError:
        print('Choice should be number')
    except Exception as e:
        print(f"An unexpected error occured: {e}")


    
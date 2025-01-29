import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
USER_FILE = Path("usr.yaml")

class configChk:

    def checkconfig(c_file=CONFIG_FILE):
        """Returns True value if the 'config.yaml' exists """
        if c_file.exists():
            return True
        else:
            return False
        
    def checkusr(c_file=USER_FILE):
        if c_file.exists():
            return True
        else:
            configChk.createusr()
            return False
        
    def createconfig():
        data=dict(IP="127.0.0.1", port=9090)
        with open(CONFIG_FILE,'w') as file:
            yaml.dump(data,file)
    
    def readconfig():
        data:dict
        with open(CONFIG_FILE,'r') as file:
            data = yaml.safe_load(file)
        return data

    def createusr(data=dict(name=None, phone=None,UUID=None)):
        
        with open(USER_FILE,'w') as file:
            yaml.dump(data,file)
        return True

    def readusr():
        """This function returns the data from user file 'usr.yaml' 
        - received data is a dict 
        ex:data=dict(name=None, phone=None,UUID=None)
        """
        if not configChk.checkusr():
            return "Error : user file doesn't Exist"
        data:dict
        with open(USER_FILE,'r') as file:
            data = yaml.safe_load(file)
        #print(data)
        return data
    
    def setUUID(UUID:str, replace:bool =False):
        """This function is used to stored the UUID received from the server in the usr.yaml file, 
        to replace the existing UUID set replace value to true"""
        if configChk.checkusr():
            data = configChk.readusr()
            if data["UUID"]!=None or replace:
                data["UUID"]=UUID
                with open(USER_FILE,'w') as file:
                    yaml.dump(data,file)
                    return "UUID Stored successfully"
            else:
                return "Error: UUID already exists want to replace set replace = True "
            
        else:
            return "Error: Usr.yaml file doesn't exist"


# print(configChk.checkconfig())
# print(configChk.checkusr())

# print(configChk.createusr())
# print(configChk.readusr())      

# print(configChk.createconfig())
# print(configChk.readconfig())  
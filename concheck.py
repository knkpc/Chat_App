import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
USER_FILE = Path("usr.yaml")
CONTACTS_FILE= Path("cont.yaml")

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
    def checkcontacts(c_file=CONTACTS_FILE):
        if c_file.exists():
            return True
        else:
            configChk.createcontacts()
            return False
    
    def createcontacts():
        temp=dict(t_usr0="0000000001", t_usr2="0000000002", t_usr3="0000000003")
        with open(CONTACTS_FILE,'w') as file:
            yaml.dump(temp,file)

    def readcontacts():
        configChk.checkcontacts()
        with open(CONTACTS_FILE,'r') as file:
            data = yaml.safe_load(file)
        
        if data:
            return data
        else:
            return {}

    def addcontact(name:str, phone:str):
        with open(CONTACTS_FILE,'r') as file:
            data = yaml.safe_load(file)
        
        if data is None:
            data={}
        data.update({name:phone})

        with open(CONTACTS_FILE,'w') as file:
            yaml.dump(data,file,default_flow_style=False)

        
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
            return {}#"Error : user file doesn't Exist"
        try:
            with open(USER_FILE,'r') as file:
                data = yaml.safe_load(file) or {}
                if not isinstance(data,dict):
                    return {}
                return data
        except (yaml.YAMLError,FileNotFoundError,IOError):
            return {}
    
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
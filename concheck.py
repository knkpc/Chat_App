import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
USER_FILE = Path("usr.yaml")

class configChk:

    def checkconfig(c_file=CONFIG_FILE):
        if c_file.exists():
            return True
        else:
            return False
        
    def checkusr(c_file=USER_FILE):
        if c_file.exists():
            return True
        else:
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

    def createusr():
        data=dict(name=None, phone=None,UUID=None)
        with open(USER_FILE,'w') as file:
            yaml.dump(data,file)

    def readusr():
        data:dict
        with open(USER_FILE,'r') as file:
            data = yaml.safe_load(file)
        return data
    
print(configChk.checkconfig())
print(configChk.checkusr())

print(configChk.createusr())
print(configChk.readusr())      

print(configChk.createconfig())
print(configChk.readconfig())  
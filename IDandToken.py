import os
import subprocess
def GetIDandToken(ipAddr): 
    Qwery = '''curl -k -D - -X POST 'https://'''+ipAddr+'''/redfish/v1/SessionService/Sessions' -H "Content-Type: application/json" -d '{ "UserName": "root", "Password": "0penBmc"}' | grep "X-Auth-Token\|Id"'''
    result = os.popen(Qwery).read()
    result = result.split("\n")
    TrueToken = result[0]
    TrueID = result[1]
    TrueID=TrueID.replace("\n","")
    TrueID = TrueID.replace('"',"",10)
    TrueID=TrueID.replace(",","")
    TrueID=TrueID.replace("Id: ","")
    TrueID = TrueID.replace(" ","",10)
    TrueToken=TrueToken.replace("\n","")
    TrueToken=TrueToken.replace("X-Auth-Token: ","")
    return TrueID, TrueToken
import os
def GetRedfishData(TrueID, TrueToken,ipAddr,SENSOR_NAME_LIST,all5):
    #sshConnectionString = "sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"
    RedFishList = []
        
    DO_LIST = []
    print("2")

        
    allRedFISh = []
    all5SP = []
    for ier in SENSOR_NAME_LIST:
        for i in all5:
            if (ier in i) and (not ".json" in i) :
                i9 = i
                    
                all5SP = all5SP + ["curl -k 'https://"+ipAddr+""+"/redfish/v1"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep -w " + "'"+"Reading" + "'"+ " | grep "+ '"' + ","+ '"' + " >> ABC.txt"]
                #StrDebug = str("curl -k 'https://"+ipAddr+"/"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep -w " + "'"+"Reading" + "'"+ " | grep "+ '"' + ","+ '"' + " >> ABC.txt")
                #print(StrDebug)
                os.system("curl -k 'https://"+ipAddr+""+"/redfish/v1"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep " + '"'+".Reading.:.*,\|message"+'"'+ " >> ABC.txt")
                
                RedFishList = RedFishList + [str("curl -k -u root:0penBmc -L https://"+ipAddr+""+i9 +  " | grep -w " + "'"+"Reading" + "'"+ " |grep "+ '"' + ","+ '"')]
                d = i9.split("/")
                d1 = d[2]
                DO_LIST = DO_LIST + [len(d1)-2]
                allRedFISh = allRedFISh + [i]
    print(all5SP)
    sur = "кол курлов"+str(len(all5SP))+"кол сенсоров redfish"+str(len(all5))+"кол сенсоров busctl"+str(len(SENSOR_NAME_LIST))
    os.system("curl -k -X DELETE 'https://"+ipAddr+"/redfish/v1/SessionService/Sessions/"+TrueID+"' -H 'X-Auth-Token: "+TrueToken+"'")
    #curl -k -X DELETE 'https://<REDFISH-HOST>/redfish/v1/SessionService/Sessions/OkFPqcVCpP' -H 'X-Auth-Token: azKvFvVfPEoHvE5a8mtv'
    print(len(all5SP))
    print("3")
    #ProgressbarState(5)
    with open("ABC.txt", "r") as file72: #чтение файла с данными на пользовательской стороне
        content52 = file72.read()
        #print(content52)
            
            
        content82 = '\n'.join(line + '!' for line in content52.splitlines())
        all51 = content82.split(("!"))
    print(all51)
    all52 = []
    for content52 in all51:
        if "message" not in content52:
            parts = content52.split('.')
            avb = parts[0]
            parts7 = parts[len(parts)-1]
            parts7 = parts7[:3]
            content52 = avb +'.'+ parts7
                
            content52.replace(",","")
            content52 = content52.replace(": null,.\n  ",": nulll")
            all52 = all52 + [content52]
        if "message" in content52:
            all52 = all52 + ["\n"+'"'+"Reading"+'"'+": NotInstalled_"]
    return all52,RedFishList
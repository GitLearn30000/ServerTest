import os
def GetRedfishData(TrueID, TrueToken,ipAddr,SENSOR_NAME_LIST,all5):
    
    #sshConnectionString = "sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"
    
    RedFishList = []
        
    DO_LIST = []
    print("2")

    filename = "ABC.txt"  
    allRedFISh = []
    #all5SP = []
    for ier in SENSOR_NAME_LIST:
        for i in all5:
            if (ier in i) and (not ".json" in i) :
                i9 = i
                    
                #all5SP = all5SP + ["curl -k 'https://"+ipAddr+""+"/redfish/v1"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep -w " + "'"+"Reading" + "'"+ " | grep "+ '"' + ","+ '"' + " >> ABC.txt"]
                #StrDebug = str("curl -k 'https://"+ipAddr+"/"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep -w " + "'"+"Reading" + "'"+ " | grep "+ '"' + ","+ '"' + " >> ABC.txt")
                size_before = os.path.getsize(filename) if os.path.exists(filename) else 0
                #print("size_before",size_before)
                os.system("curl -k 'https://"+ipAddr+""+"/redfish/v1"+i9+ "' -H "+ "'X-Auth-Token: "+TrueToken+"'"+ " | grep " + '"'+".Reading.:.*,\|message"+'"'+ " >> ABC.txt")
                size_after = os.path.getsize(filename)
                print("size_after",size_after)
                if size_after == size_before:
                    os.system(f'echo "SSLerror" >> ABC.txt')
                RedFishList = RedFishList + [str("curl -k -u root:0penBmc -L https://"+ipAddr+""+i9 +  " | grep -w " + "'"+"Reading" + "'"+ " |grep "+ '"' + ","+ '"')]
                d = i9.split("/")
                d1 = d[2]
                DO_LIST = DO_LIST + [len(d1)-2]
                allRedFISh = allRedFISh + [i]
    #print(all5SP)
    #sur = "кол курлов"+str(len(all5SP))+"кол сенсоров redfish"+str(len(all5))+"кол сенсоров busctl"+str(len(SENSOR_NAME_LIST))
    os.system("curl -k -X DELETE 'https://"+ipAddr+"/redfish/v1/SessionService/Sessions/"+TrueID+"' -H 'X-Auth-Token: "+TrueToken+"'")
    #curl -k -X DELETE 'https://<REDFISH-HOST>/redfish/v1/SessionService/Sessions/OkFPqcVCpP' -H 'X-Auth-Token: azKvFvVfPEoHvE5a8mtv'
    #print(len(all5SP))
    print("3")
    #ProgressbarState(5)
    with open("ABC.txt", "r") as ClientDataValues: #чтение файла с данными на пользовательской стороне
        ClientDataStrings = ClientDataValues.read()
        print(ClientDataStrings)
            
            
        FixClientDataStrings = '\n'.join(line + '!' for line in ClientDataStrings.splitlines())
        SplitClientDataStrings = FixClientDataStrings.split(("!"))
    print(SplitClientDataStrings)
    FinalClientData = []
    for DataString in SplitClientDataStrings:
        if ("message" not in DataString) and ("SSLerror" not in DataString):
            SplitDataString = DataString.split('.')
            BeforePointDataString = SplitDataString[0]
            FixDataString = SplitDataString[len(SplitDataString)-1]
            FixDataString = FixDataString[:3]
            DataString = BeforePointDataString +'.'+ FixDataString
                
            DataString.replace(",","")
            DataString = DataString.replace(": null,.\n  ",": nulll")
            if DataString != ".":
                FinalClientData = FinalClientData + [DataString]
        if "was not found" in DataString:
            FinalClientData = FinalClientData + ["\n"+'"'+" Reading"+'"'+": NotInstalled_"]#OpenSSL SSL_read: error
        if ("SSLerror" in DataString):#not found
            FinalClientData = FinalClientData + ["\n"+'"'+" Reading"+'"'+": SSL_Error_"]
        #if ("not found" in ClientDataStrings):#not found
            #FinalClientData = FinalClientData + ["\n"+'"'+"Reading"+'"'+": not found"]
    #print(FinalClientData)
    
    return FinalClientData,RedFishList
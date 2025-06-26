import os
def GetBusctlData(DBusQwery_SP,ipAddr):
        
        #os.remove("ABC.txt") #удаление файлов
        #os.remove("CBA.txt")
        #ProgressbarState(2)
        
        #selected_items = ["PSU1", "/AQUARIUS_AQC621AB_Baseboard/", "PSU2", "/AQUARIUS_AQC621AB_Chassis/", "/AQFPB_FFC/"]    
        
        
        
        NUMBER_OF_COUNT_SENSORS = 0
        
        
        
        
        
        DBusQwery_SPEND = []
        for qwe23 in DBusQwery_SP:
            DBusQwery_SPEND = DBusQwery_SPEND + [str("echo 1  && ")+qwe23+str(" &>> CBA.txt\n")]
        #ProgressbarState(3)
        myString = ''.join(DBusQwery_SPEND)
        f = open( 'Complete.txt', 'w' )
        f.write('#!/bin/sh\n')
        f.write(myString)
        f.close()
        print(NUMBER_OF_COUNT_SENSORS)
        sshConnectionString = "sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"
        scpConnectionShortString = "sshpass -p 0penBmc scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        os.system(sshConnectionString+ipAddr+" rm CBA.txt")
        os.system("chmod +x Complete.txt")
        os.system(scpConnectionShortString+" ./Complete.txt root@"+ipAddr+":/home/root/Complete.txt")
        os.system(sshConnectionString+ipAddr+" './Complete.txt'")
        os.system(scpConnectionShortString+" root@"+ipAddr+":/home/root/CBA.txt ./")
    
        with open("CBA.txt", "r") as ServerValues: #чтение файла с данными на серверной стороне
                ServerValuesStrings = ServerValues.read()
                #print(ServerValuesStrings)
                FixServerValuesStrings = '\n'.join(line + '!' for line in ServerValuesStrings.splitlines())
                SplitServerValuesStrings = FixServerValuesStrings.split(("!"))
        print(SplitServerValuesStrings)
        FinalServerData = []
        for ServerIndexValue in SplitServerValuesStrings:
            if "." not in ServerIndexValue:
                ServerIndexValue=ServerIndexValue+".00"
            parts = ServerIndexValue.split('.')
            FixServerIndexValue = parts[0]
            ServerIndexValueAfterPoint = parts[len(parts)-1]
            ServerIndexValueAfterPoint = ServerIndexValueAfterPoint[:2]
            if ServerIndexValueAfterPoint != "":
                ServerIndexValue = FixServerIndexValue +'.'+ ServerIndexValueAfterPoint
            if ServerIndexValueAfterPoint == "":
                ServerIndexValue = FixServerIndexValue +'.'+ "00"
            ServerIndexValue = ServerIndexValue.replace(" nan.00"," nan")
            #while "\nd " in ServerIndexValue:
                #ServerIndexValue = ServerIndexValue.replace("\nd ","")
            if "Failed to get property Value on interface xyz" not in ServerIndexValue and ServerIndexValue != ".00":
                FinalServerData = FinalServerData + [ServerIndexValue]
            if "Failed to get property Value on interface xyz" in ServerIndexValue:
                FinalServerData = FinalServerData + ["\nd NotInstalled"]
        #print(FinalServerData)
        #ProgressbarState(4)
        #ProgressbarState(4)
        
        #print((SENSOR_NAME_LIST))
        return FinalServerData
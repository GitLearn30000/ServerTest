import os
def funct4(DBusQwery_SP,ipAddr):
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
        os.system("chmod +x Complete.txt")
        os.system(scpConnectionShortString+" ./Complete.txt root@"+ipAddr+":/home/root/Complete.txt")
        os.system(sshConnectionString+ipAddr+" './Complete.txt'")
        os.system(scpConnectionShortString+" root@"+ipAddr+":/home/root/CBA.txt ./")
    
        with open("CBA.txt", "r") as file79: #чтение файла с данными на серверной стороне
                content58 = file79.read()
                #print(content58)
                content89 = '\n'.join(line + '!' for line in content58.splitlines())
                all58 = content89.split(("!"))
        print(all58)
        all59 = []
        for contenr59 in all58:
            if "." not in contenr59:
                contenr59=contenr59+".00"
            parts = contenr59.split('.')
            avb = parts[0]
            parts7 = parts[len(parts)-1]
            parts7 = parts7[:2]
            if parts7 != "":
                contenr59 = avb +'.'+ parts7
            if parts7 == "":
                contenr59 = avb +'.'+ "00"
            contenr59 = contenr59.replace(" nan.00"," nan")
            #while "\nd " in contenr59:
                #contenr59 = contenr59.replace("\nd ","")
            if "Failed to get property Value on interface xyz" not in contenr59:
                all59 = all59 + [contenr59]
            if "Failed to get property Value on interface xyz" in contenr59:
                all59 = all59 + ["\nd NotInstalled"]
        print(all59)
        #ProgressbarState(4)
        
        #print((SENSOR_NAME_LIST))
        return all59
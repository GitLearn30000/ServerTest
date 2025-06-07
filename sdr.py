import os
def funct1(ipAddr):
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool sdr"+" > Sdr.txt") #ipmitool fru | grep "FRU Device Description"> PlateNamesList.txt
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/Sdr.txt ./") #ipmitool power status
        
        with open("Sdr.txt", "r") as fileSDR: #чтение файла с данными на пользовательской стороне
            contentSDR = fileSDR.read()
            print(contentSDR)
                
            
            SDR82 = '\n'.join(line + '!' for line in contentSDR.splitlines())
            allSDR = SDR82.split(("!"))
        print(allSDR)
        cSDR = []
        for i in allSDR:
            i = i.replace("| ns","")
            i = i.replace("| ok","")
            i = i.replace("| nr","")
            while " " in i:
                i = i.replace(" ","")
                
            cSDR =cSDR+[i]
        print(cSDR)
        return cSDR,allSDR
import os
def GetIpmiData(ipAddr):
        os.system("sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"+ipAddr+" ipmitool sdr"+" > Sdr.txt") #ipmitool fru | grep "FRU Device Description"> PlateNamesList.txt
        os.system("sshpass -p 0penBmc scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"+ipAddr+":/home/root/Sdr.txt ./") #ipmitool power status
        
        with open("Sdr.txt", "r") as fileSDR: #чтение файла с данными на пользовательской стороне
            contentSDR = fileSDR.read()
            #print(contentSDR)
                
            
            SDR82 = '\n'.join(line + '!' for line in contentSDR.splitlines())
            allSDR = SDR82.split(("!"))
        #print(allSDR)
        cSDR = []
        for FixSDRValue in allSDR:
            FixSDRValue = FixSDRValue.replace("| ns","")
            FixSDRValue = FixSDRValue.replace("| ok","")
            FixSDRValue = FixSDRValue.replace("| nr","")
            while " " in FixSDRValue:
                FixSDRValue = FixSDRValue.replace(" ","")
                
            cSDR =cSDR+[FixSDRValue]
        #print(cSDR)
        return cSDR,allSDR
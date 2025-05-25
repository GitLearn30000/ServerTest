import os
import sys
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#10.12.140.137
def CatMeow(ipAddr):
    for filename in ["CBA.txt", "ABC.txt","Sdr.txt", "PowerServer.txt"]:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✅ Удалено: {filename}")
        else:
            print(f"❌ Не найдено: {filename}")
    os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool power status"+" > PowerServer.txt")
    os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/PowerServer.txt ./")
    with open("PowerServer.txt", "r") as filePowerServer: #чтение файла с данными на пользовательской стороне
        contentPowerServer = filePowerServer.read()
        print(contentPowerServer)
            
        
        PowerServer82 = '\n'.join(line + '!' for line in contentPowerServer.splitlines())
        allPowerServer = PowerServer82.split(("!"))
    print(allPowerServer[0])

    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #тут редактировать обработку Json для RedFish
    
    # Загрузка данных из файла paths.json
    with open('paths.json', 'r', encoding='utf-8') as file:
        MeoW0data = json.load(file)

    # Инициализация пустых списков для хранения значений
    MeoW0MEowNotMore = []
    OmeowDoSensor = []
    DBUSMEOWLINK = []
    StateServer = []
    serverstate = ""
    if "is on" in allPowerServer[0]:
        serverstate = "on"
    else:
        serverstate = "off"
    # Переменная состояния сервера
    stateMyServer = serverstate  # Замените на "on" для тестирования другого состояния

    # Функция для рекурсивного поиска значений
    def MeoW0extract_paths(MeoW0current_data):
        if isinstance(MeoW0current_data, dict):
            # Проверяем наличие нужных ключей в самом словаре
            if "PowerState" in MeoW0current_data:
                power_state = MeoW0current_data["PowerState"]
                if stateMyServer == "off" and power_state == "off":
                    add_values(MeoW0current_data)  # Добавляем только данные с PowerState "off"
                elif stateMyServer == "on":
                    add_values(MeoW0current_data)  # Добавляем все данные при "on"
            else:
                # Если ключа "PowerState" нет, продолжаем рекурсивный вызов
                for MeoW0key, MeoW0value in MeoW0current_data.items():
                    MeoW0extract_paths(MeoW0value)
        elif isinstance(MeoW0current_data, list):
            for MeoW0item in MeoW0current_data:
                MeoW0extract_paths(MeoW0item)

    # Функция для добавления значений в списки
    def add_values(data):
        if "redfishPath" in data:
            MeoW0MEowNotMore.append(data["redfishPath"])
        if "sensorName" in data:
            OmeowDoSensor.append(data["sensorName"])
        if "dbusPath" in data:
            DBUSMEOWLINK.append(data["dbusPath"])
        if "PowerState" in data:
            StateServer.append(data["PowerState"])

    # Начало извлечения
    MeoW0extract_paths(MeoW0data)

    # Вывод результата
    print("redfishPath values:", MeoW0MEowNotMore, len(MeoW0MEowNotMore))
    print("sensorName values:", OmeowDoSensor, len(OmeowDoSensor))
    print("dbusPath values:", DBUSMEOWLINK, len(DBUSMEOWLINK))
    print("PowerState values:", StateServer, len(StateServer))

    # Если вам нужно сохранить все значения redfishPath в переменной all5
    all5 = MeoW0MEowNotMore
    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    MeowOn()
    SENSOR_NAME_LIST = OmeowDoSensor
    end_dict = {}
    def funct0():
        os.system("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 > Extra.txt && echo ------- >> Extra.txt")
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        os.system("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'\\'+'""'+" >> Extra.txt && echo ------- >> Extra.txt")
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity "+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/Extra.txt ./")
        print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 > Extra.txt && echo ------- >> Extra.txt")
        print("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'\\'+'""'+" >> Extra.txt && echo ------- >> Extra.txt")
        print("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity "+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        with open("Extra.txt", "r") as ExtraTokenfile79:
            ExtraTokencontent58 = ExtraTokenfile79.read()
            print(ExtraTokencontent58)
            
            ExtraTokencontent89 = '\n'.join(line + '!' for line in ExtraTokencontent58.splitlines())
            #ExtraTokenall58 = ExtraTokencontent89.split(("!"))
            #ExtraGAV = []
            print("ExtraTokencontent89: ",ExtraTokencontent89)
            if len(ExtraTokencontent89) >=1:
                aLLCatAllow = ExtraTokencontent89.split("-------")
                print(aLLCatAllow)
                allREWQ = aLLCatAllow[0]
                allREWQRD = allREWQ.split("\n")
                SOAQWER = []
                for i in range (len(allREWQRD)-1):
                        if i == 0:
                            QWERTYUIOP = 0
                        if i >= 1:
                            tmpYTT = allREWQRD[i]
                            while " " in tmpYTT:
                                tmpYTT = tmpYTT.replace(" ","")
                            
                            tmpYTT = tmpYTT.replace(",!","")
                            while "!" in tmpYTT:
                                tmpYTT = tmpYTT.replace("!","")
                            #нужно перевести tmpYTT в число ,обрезать до двух знаков после запятой и  перевести снова в строку, и нужно пропускать строки "null"
                            if tmpYTT.lower() != "null" and tmpYTT != "" and tmpYTT != '':
                            # Attempt to convert the cleaned string to a float
                    
                                number = float(tmpYTT)
                                # Format the number to two decimal places and convert it back to a string
                                formatted_number = f"{number:.2f}"
                                # Append to the SOAQWER list
                                SOAQWER = SOAQWER + [str(formatted_number)]
                            if tmpYTT.lower() == "null":
                                SOAQWER = SOAQWER + [str("null")]
                                
                            
                print(SOAQWER)
                NewValueContinued =   aLLCatAllow[1]
                NewValueContinued = NewValueContinued.replace("Temperatures                               property  ad        ","")
                NewValueContinued = NewValueContinued.replace("                                            emits-change!\n","")
                NewMeowASQ = NewValueContinued.split(" ")
                JNFJNF = []
                for i in range (len(NewMeowASQ)):
                        if i == 0:
                            QWERTYUIOP = 0
                        if i >= 1:
                            JNFJNF = JNFJNF + [NewMeowASQ[i]]
                print(JNFJNF)
                HKLKJH = aLLCatAllow[2]
                HKLKJH=HKLKJH.replace('Humidity',"")
                HKLKJH=HKLKJH.replace(':',"")
                HKLKJH=HKLKJH.replace(',',"")
                HKLKJH=HKLKJH.replace('!',"")
                while '"' in HKLKJH:
                    HKLKJH=HKLKJH.replace('"',"")
                while " " in HKLKJH:
                    HKLKJH=HKLKJH.replace(" ","")
                HKLKJH=HKLKJH.replace("\n","")
                number = float(HKLKJH)
                                
                HKLKJH = f"{number:.2f}"
                print(HKLKJH)
                GNXDTV = aLLCatAllow[3]
                GNXDTV=GNXDTV.replace("property  d","")
                GNXDTV=GNXDTV.replace("emits-change","")
                GNXDTV=GNXDTV.replace(".Humidity","")
                while "!" in GNXDTV:
                    GNXDTV=GNXDTV.replace("!","")
                while " " in GNXDTV:
                    GNXDTV=GNXDTV.replace(" ","")
                GNXDTV=GNXDTV.replace("\n","")
                print(GNXDTV)
                end_dict[str("HEATER_HUMID")+"!"+str(HKLKJH)+"!"+str(GNXDTV)+ "!-"] = "IR-AX-HU"
                JKCFHHJ = []
                for i in range(len(SOAQWER)):
                    JKCFHHJ = JKCFHHJ + [str(SOAQWER[i])+" "+str(JNFJNF[i])+ " -"]
                    end_dict[str("HEATER_TEMP-"+str(i))+"!"+str(JNFJNF[i])+"!"+str(SOAQWER[i])+ "!-"] = "IR-AX-HU"+str(i)

                print(JKCFHHJ)
        return end_dict
    #ProgressMeow(0)
    
    os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" 'rm Extra.txt'")
    
    #ipmitool sdr
    def funct1():
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool sdr"+" > Sdr.txt") #ipmitool fru | grep "FRU Device Description"> ErrorMeow.txt
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
    


    def funct2():
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool fru | grep "+'"'+"FRU Device Description"+'"'+" > ErrorMeow.txt") #ipmitool fru | grep "FRU Device Description"> ErrorMeow.txt
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/ErrorMeow.txt ./")
        with open("ErrorMeow.txt", "r") as fileMeow: #чтение файла с данными на пользовательской стороне
            contentMeow = fileMeow.read()
            print(contentMeow)
                
            
            Meow82 = '\n'.join(line + '!' for line in contentMeow.splitlines())
            allMeow = Meow82.split(("!"))
        print(allMeow)
        #busctl introspect xyz.openbmc_project.FruDevice /xyz/openbmc_project/FruDevice/AQC621AB
        
        CorrectMeow = []
        for MeowQ in allMeow:
            Meow2 = MeowQ.replace("FRU Device Description : ","")
            
            Meow3 = Meow2.split("(")
            Meow4=Meow3[0]
            Meow4 = Meow4.replace(" ","")
            Meow4 = Meow4.replace("\n","")
            if Meow4 != "":
                Meow4=Meow4.replace("BuiltinFRUDevice","AQUARIUS_AQC621AB")
                Meow4=Meow4.replace("AQFPB-FFC","AQFPB_FFC")#AQRZ2_U4P1_R_TMP
                Meow4=Meow4.replace("AQRZ2-U4P1-R","AQRZ2_U4P1_R")
                CorrectMeow = CorrectMeow + [Meow4]
        selected_items = CorrectMeow
        return selected_items,CorrectMeow
    
        #CorrectMeow = CorrectMeow + ["AQUARIUS_AQC621AB"]
    def funct3():
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool fru > MeowSENSOR.txt") #ipmitool fru | grep "FRU Device Description"> ErrorMeow.txt
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/MeowSENSOR.txt ./")
        #CorrectMeow = CorrectMeow +  ["Server_Chassis"]
        with open("MeowSENSOR.txt", "r") as MeowSENSOR: #чтение файла с данными на пользовательской стороне
            contentMeowSENSOR= MeowSENSOR.read()
            print(contentMeowSENSOR)
            contentMeowSENSOR=contentMeowSENSOR.replace("Product Area Checksum : OK","") 
            contentMeowSENSOR=contentMeowSENSOR.replace("Chassis Area Checksum : OK","")      
            contentMeowSENSOR=contentMeowSENSOR.replace("Board Area Checksum   : OK","")
            contentMeowSENSOR=contentMeowSENSOR.replace("Product Asset Tag     : asset_tag_vv","")
            contentMeowSENSOR=contentMeowSENSOR.replace("Device not present (Requested sensor, data, or record not found)","ERROR : NoData")
            #Device not present (Requested sensor, data, or record not found)
            MeowMeowSENSOR = '\n'.join(line + '!' for line in contentMeowSENSOR.splitlines())
            
            allMeowing = MeowMeowSENSOR.split(("FRU Device Description :"))
        print(allMeowing)
        
        MeowSP = []
        MeowExtra = ""
        #MeowCount = 0
        for QMEOW in allMeowing:
            
            
            if "BuiltinFRUDevice" not in QMEOW:
                while "!" in QMEOW:
                    QMEOW = QMEOW.replace("!","")
            if "BuiltinFRUDevice" in QMEOW:
                while "!" in QMEOW:
                    QMEOW = QMEOW.replace("!","")
                MeowExtra = QMEOW
            if "" != QMEOW:
                MeowSP = MeowSP + [QMEOW]
                
        MeowSP = MeowSP + [MeowExtra]
        #ipAddr = "10.12.140.137"
        print(MeowSP)
        
        return allMeowing,MeowSP
    
    #exit()
    print("0")
    def funct4():
        #os.remove("ABC.txt") #удаление файлов
        #os.remove("CBA.txt")
        #ProgressMeow(2)
        
        #selected_items = ["PSU1", "/AQUARIUS_AQC621AB_Baseboard/", "PSU2", "/AQUARIUS_AQC621AB_Chassis/", "/AQFPB_FFC/"]    
        
        
        
        NUMBER_OF_COUNT_SENSORS = 0
        
        
        
        
        
        DBUSMEOWLINKEND = []
        for qwe23 in DBUSMEOWLINK:
            DBUSMEOWLINKEND = DBUSMEOWLINKEND + [str("echo 1  && ")+qwe23+str(" &>> CBA.txt\n")]
        #ProgressMeow(3)
        myString = ''.join(DBUSMEOWLINKEND)
        f = open( 'Complete.txt', 'w' )
        f.write('#!/bin/sh\n')
        f.write(myString)
        f.close()
        print(NUMBER_OF_COUNT_SENSORS)
        os.system("chmod +x Complete.txt")
        os.system("sshpass -p 0penBmc scp ./Complete.txt root@"+ipAddr+":/home/root/Complete.txt")
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" './Complete.txt'")
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/CBA.txt ./")
    
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
        #ProgressMeow(4)
        
        print((SENSOR_NAME_LIST))
        return all59
    #all5 = ['/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_A_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_A_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_E_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_W_TMP','/Chassis/AQUARIUS_AQC621AB_Chassis/PowerSubsystem/PowerSupplies/ASPOWER_1600W_PSU_1', '/Chassis/AQUARIUS_AQC621AB_Chassis/PowerSubsystem/PowerSupplies/ASPOWER_1600W_PSU_2', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU1_IN_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU1_OUT_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU2_IN_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU2_OUT_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_PSU1_FAN_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_PSU2_FAN_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN1_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN2_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN5_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN6_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_PSU1_FAN_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_PSU2_FAN_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN1_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN2_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN5_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN6_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU1_IN_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU1_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU2_IN_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU2_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/temperature_PSU1_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/temperature_PSU2_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU1_IN_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU1_OUT_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU2_IN_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU2_OUT_VLT', '/Chassis/AQFPB_FFC/Sensors/temperature_AQFPB_FFC_TMP', '/Chassis/AQRZ2_U4P1_R/Sensors/temperature_AQRZ2_U4P1_R_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/power_PSU_TTL_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_DTS_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_P1V8_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_PVCCIN_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_PVCCIO_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_B_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_C_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_D_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_E_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_F_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_G_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_H_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_PVDDQ_ABCD_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_PVDDQ_EFGH_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_TEMP1_OUT_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_TEMP2_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_3V_BAT_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_P1V8_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCANA_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCIN_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCIO_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCSA_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P12V_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P1V05_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P1V8_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P3V3_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVDDQ_ABCD_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVDDQ_EFGH_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVNN_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVPP_ABCD_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVPP_EFGH_VLT', '/Chassis/P425G410G8TS81_XR_Silicom_STS4/Sensors/temperature_SIL_STS4_TMP']
    # Загрузка данных из файла paths.json
    
    
    def funct5():
        GS = []
        
        DO_LIST = []
        print("2")
        link_sp = []
        os.system("curl -k -D - -X POST 'https://"+ipAddr+"/redfish/v1/SessionService/Sessions"             +   "'"+" -H "+'"'+"Content-Type: application/json"+'"'+" -d '"+'{'+' "'+"UserName"+'"'+": "+'"'+"root"+'"'+", "+'"'+"Password"+'"'+": "+'"'+"0penBmc"+'"'+ '}'+"' | grep "+'"'+"X-Auth-Token:"+'"'+" > MeowToken.txt")
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/MeowToken.txt ./")
        with open("MeowToken.txt", "r") as Tokenfile79: #чтение файла с данными на серверной стороне
                Tokencontent58 = Tokenfile79.read()
                print(Tokencontent58)
                Tokencontent89 = '\n'.join(line + '!' for line in Tokencontent58.splitlines())
                Tokenall58 = Tokencontent89.split(("!"))
        print(Tokenall58)
        TrueToken = Tokenall58[0]
        TrueToken = TrueToken.replace("X-Auth-Token: ","")
        os.system("curl -k -D - -X POST 'https://"+ipAddr+"/redfish/v1/SessionService/Sessions"             +   "'"+" -H "+'"'+"Content-Type: application/json"+'"'+" -d '"+'{'+' "'+"UserName"+'"'+": "+'"'+"root"+'"'+", "+'"'+"Password"+'"'+": "+'"'+"0penBmc"+'"'+ '}'+"' | grep "+'"'+"Id"+'"'+" > MeowID.txt")
        os.system("sshpass -p 0penBmc scp root@"+ipAddr+":/home/root/MeowID.txt ./")
        with open("MeowID.txt", "r") as IDfile79: #чтение файла с данными на серверной стороне
                IDcontent58 = IDfile79.read()
                print(IDcontent58)
                IDcontent89 = '\n'.join(line + '!' for line in IDcontent58.splitlines())
                IDall58 = IDcontent89.split(("!"))
        print(IDall58)
        TrueID = IDall58[0]
        while " " in TrueID:
            TrueID = TrueID.replace(" ","")
        while '"' in TrueID:
            TrueID = TrueID.replace('"',"")
        TrueID = TrueID.replace(":","")
        TrueID = TrueID.replace(",","")
        TrueID = TrueID.replace("Id","")
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
                    link_sp = link_sp + ["curl -k -u root:0penBmc -L https://"+ipAddr+""+"/redfish/v1"+i9 +  " | grep -w " + "'"+"Reading" + "'"+ " |grep "+ '"' + ","+ '"']
                    GS = GS + [str("curl -k -u root:0penBmc -L https://"+ipAddr+""+i9 +  " | grep -w " + "'"+"Reading" + "'"+ " |grep "+ '"' + ","+ '"')]
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
        #ProgressMeow(5)
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
        return all52,GS
    
    def run_all_functions():
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(funct5): 'funct5',
                executor.submit(funct4): 'funct4',
                executor.submit(funct2): 'funct2',
                executor.submit(funct3): 'funct3',
                executor.submit(funct1): 'funct1',
                executor.submit(funct0): 'funct0'
            }

            results = {}
            for future in as_completed(futures):
                func_name = futures[future]
                try:
                    results[func_name] = future.result()
                except Exception as e:
                    print(f"{func_name} вызвала исключение: {e}")
        
        # Распаковка результатов
        all52, GS = results['funct5']
        all59 = results['funct4']
        selected_items,CorrectMeow = results['funct2']
        allMeowing, MeowSP = results['funct3']
        cSDR, allSDR = results['funct1']
        end_dict = results['funct0']

        return all52, GS, all59, CorrectMeow, selected_items, allMeowing, MeowSP, cSDR, allSDR, end_dict

    # Вызов
    all52, GS, all59, CorrectMeow, selected_items, allMeowing, MeowSP, cSDR, allSDR, end_dict = run_all_functions()
    
    
    dub = []
    BEST_LEN = 0
    for o in SENSOR_NAME_LIST:
        if BEST_LEN < len(o):
            BEST_LEN = len(o)
    MEOWWW_LEN = 0
    for q in all52:
        if MEOWWW_LEN < len(q):
            MEOWWW_LEN = len(q)
    nnn = GS
    MeowForJson = []
    DebugList = []
    
    for i in range(len(all52)-1): #сравнение данных и вывод на экран
        ClienT = all52[i].split(":")
        ClienT = ClienT[1]
        ClienT = ClienT[:-1]
        SerVer1 = all59[i].split(" ")
        SerVer2 = SerVer1[1]
        ert = 0
        #AQRZ2_U4P1_R_TMP
        GSS = GS[i]
        MQ = GS[i]
        
        
        if "ACC100" in GSS or "SIL_STS4" in GSS:
            GSS = GSS + "https://10.12.140.137/redfish/v1/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors"
        DebugList = DebugList + [SENSOR_NAME_LIST[i]]
        
            
            

        for gt in selected_items:
            if ert == 0:
                for nn in GS:
                    if ert == 0:
                        if (gt in nn):
                            if ert == 0:
                                if gt in GSS:
                                    for NM in GS:
                                        for meoow in cSDR:
                                            if OmeowDoSensor[i] in NM and "/chassis" not in NM and "/inventory" not in NM and OmeowDoSensor[i] in meoow: # and "/chassis" not in NM and "/inventory" not in NM and "/sensors" not in NM and "/powering" not in NM and "/contained_by" not in NM
                                                print(i)
                                                #print(len(all52))
                                                #print(len(all59))
                                                
                                                print("gt: ",gt)
                                                NM = NM.replace("\n","")
                                                while "|" in NM:
                                                    NM = NM.replace("|","")
                                                NM = NM.replace("-","")
                                                NM = NM.replace("`","")
                                                while " " in NM:
                                                    NM = NM.replace(" ","")
                                                #print("nn: ",nn)
                                                #print("SPLIST[i]: ",SPLIST[i])#cSDR
                                                
                                                
                                                SerVer2 = SerVer2.replace("null,.","null")
                                                ClienT = ClienT.replace("nan.00","nan")
                                                
                                                #print(SENSOR_NAME_LIST[i] + ": "+ "Client:"+ClienT  + "|" + "Server:"+ SerVer2 + "======" + NM)
                                                SDF = len(SENSOR_NAME_LIST[i])
                                                Meow = BEST_LEN - SDF
                                                tmp_str = ""
                                                tmp_str1 = ""
                                                for ex in range(Meow):
                                                    tmp_str = tmp_str + " "
                                                SDF1 = len(ClienT)
                                                Meow1 = MEOWWW_LEN - SDF1
                                                #tmp_str = ""
                                                az = len(str("\n   Reading : "))
                                                for eu in range(Meow1-az):
                                                    tmp_str1 = tmp_str1 + " "

                                                meoow=meoow.replace("\n","")
                                                meoow=meoow.replace(str(OmeowDoSensor[i]+"|"),"")
                                                meoow=meoow.replace(str("degreesC"),"°C")
                                                meoow=meoow.replace(str("Volts"),"V")#percent
                                                meoow=meoow.replace(str("percent"),"%")
                                                meoow=meoow.replace(str("Watts"),"W")
                                                meoow=meoow.replace(str("Amps"),"A")
                                                meoow=meoow.replace(str("RPM")," RPM")
                                                MeowReplace = GSS
                                                MeowReplace=MeowReplace.replace("AQUARIUS_AQC621AB_Chassis","")
                                                MeowReplace=MeowReplace.replace("AQUARIUS_AQC621AB_Baseboard","")#SIL_STS4
                                                #MeowReplace=MeowReplace.replace("AQFPB_FFC"," AQFPB-FFC ")
                                                #MeowReplace=MeowReplace.replace("AQRZ2_U4P1_R_TMP","AQRZ2_U4P1_R")
                                                MeowReplace=MeowReplace.replace("SIL_STS4","Server_Chassis")#SIL_STS4_TMP
                                                MeowReplace=MeowReplace.replace("SYS_FAN1_RPM","Server_Chassis")#AQRZ2_U4P1_R_TMP
                                                MeowReplace=MeowReplace.replace("SYS_FAN2_PWM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN1_PWM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN6_PWM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN5_RPM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN6_RPM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN5_PWM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("SYS_FAN2_RPM","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("ACC100_A_TMP","1Server_Chassis1")
                                                MeowReplace=MeowReplace.replace("ACC100_E_TMP","2Server_Chassis2")
                                                MeowReplace=MeowReplace.replace("ACC100_W_TMP","3Server_Chassis3")
                                                MeowReplace=MeowReplace.replace("PSU_TTL_OUT_PWR","Server_Chassis")
                                                MeowReplace=MeowReplace.replace("PVPP_ABCD_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVNN_PCH_AX_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVDDQ_ABCD_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_A_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_B_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_F_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_C_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_H_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVDDQ_EFGH_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCIO_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("P1V8_PCH_AX_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("3V_BAT_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("P12V_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCANA_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("TEMP1_OUT_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCIN_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCIO_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVDDQ_EFGH_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_P1V8_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVDDQ_ABCD_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_G_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("P1V05_PCH_AX_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PVPP_EFGH_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCIN_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_D_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_DTS_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("DDR4_E_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_PVCCSA_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("P3V3_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("CPU1_P1V8_VLT"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("TEMP2_IN_TMP"," Server_Board ")
                                                MeowReplace=MeowReplace.replace("PSU1_IN_VLT","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_OUT_PWR","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_OUT_VLT","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_IN_PWR","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_IN_AMP","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_FAN_RPM","PSU1")
                                                MeowReplace=MeowReplace.replace("fanpwm_PSU1_FAN_PWM","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_OUT_AMP","PSU1")
                                                MeowReplace=MeowReplace.replace("PSU1_IN_TMP","PSU1")
                                                MeowReplace=MeowReplace.replace("fanpwm_PSU2_FAN_PWM","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_IN_VLT","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_OUT_AMP","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_FAN_RPM","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_IN_PWR","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_OUT_VLT","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_OUT_PWR","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_IN_TMP","PSU2")
                                                MeowReplace=MeowReplace.replace("PSU2_IN_AMP","PSU2")
                                                
                                                xmSensor = str(SENSOR_NAME_LIST[i] + "!"+ClienT  +  "!"+ SerVer2 +"!")
                                                while " " in xmSensor:
                                                    xmSensor=xmSensor.replace(" ","")
                                                end_dict[xmSensor+str(meoow)] = MeowReplace#+ "!!!!!!"+GS[i]
                                                
                                                dub = dub + [xmSensor+str(meoow)]
                                                
                                                #MeowForJson = MeowForJson + [str(SENSOR_NAME_LIST[i]+ "&" + LIST_FOR_DICT_QUERY_TO_SERVER[i]+"&"+str(allRedFISh[i]))]
                                                ert = 1
    os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" rm CBA.txt")
    
    print(len(SENSOR_NAME_LIST))
    print(len(GS))
    print(GS)
    print(all59)
    #ProgressMeow(6)
        
    #print(DO_LIST)
    #print("Отмеченные предметы:", items)
        
    #exit()
    os.remove("ABC.txt") #удаление файлов
    os.remove("CBA.txt") #удаление файлов
    os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" touch CBA.txt") #создание пустого файла
    
    x = selected_items



    #Failed to get property Value on interface xyz


    z = end_dict
    
    #{"iphone": "AQUARIUS_AQC621AB_Chassis/", "ipad": "AQUARIUS_AQC621AB_Chassis/", "iead": "AQUARIUS_AQC621AB_Baseboard/"}
    print(all52)
    print(all59)
    print(CorrectMeow)
    MeowOff()
    
    
    
    ExtraGAV = []
    ProgressMeow(1)
    ProgressMeow(2)
    ProgressMeow(3)
    ProgressMeow(4)
    ProgressMeow(5)
    ProgressMeow(6)
    ProgressMeow(7)
   

    DefMeow = 0
    for w in CorrectMeow:
        z["NoData!NoData!NoData"+str(DefMeow)] = w
        DefMeow = DefMeow + 1
    x = x + ["Server_Chassis"]
    FinalMeow = []
    MeowCount = 0
    for cat in x:
        print(cat)
        if MeowCount == 0:
            FinalMeow = FinalMeow + ["Server_Board"]
        if MeowCount >= 1:
            FinalMeow = FinalMeow + [cat]
        MeowCount = MeowCount + 1
    x = FinalMeow
    print(x)
    print(z)
    print(all5)
    print("-------------------")
    print(cSDR)
    print("all52",len(all52))
    print("all59",len(all59))
    print("cSDR",len(cSDR))
    print(all52)
    print(all59)
    print("-------------------")
    print("-------------------")
    print("-------------------")
    #print(cONLY_NAME_SENSOR)
    #print(len(cONLY_NAME_SENSOR))
    print(all59)
    print("-------------------")
    print("-------------------")
    print("-------------------")
    #print(sur)
    #print(end_dict)
    print(SENSOR_NAME_LIST)
    #print(GS)
    # Преобразуем строки в список словарей
    data = MeowForJson
    result = []
    '''for item in data:
        parts = item.split("&")
        result.append({
            "sensorName": parts[0],
            "dbusPath": parts[1],
            "redfishPath": parts[2]
        })

    # Сохраняем в файл paths.json
    with open("paths.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Данные успешно сохранены в paths.json")'''
    #print(all5SP)
    #print(end_dict)
    print(SENSOR_NAME_LIST)
    print(DebugList)
    
    print(allSDR)
    #print("Extra: ",ExtraGAV)#HEATER_TEMP
    #print("HEATER_TEMP FISH: ",ExtraGAV[0])
    #print("HEATER_TEMP BUS: ",ExtraGAV[1])
    #print("HEATER_HUMID FISH: ",ExtraGAV[2])
    #print("HEATER_HUMID BUS: ",ExtraGAV[3])
    #if len(ExtraGAV) >= 4:
        #z["HEATER_TEMP "+str(ExtraGAV[0])+" "+ str(ExtraGAV[1])+" -"] = "IR-AX-HU1"
        #z["HEATER_HUMID "+str(ExtraGAV[2])+" "+ str(ExtraGAV[3])+" -"] = "IR-AX-HU2"
    #print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 | grep [0-9] >> Extra.txt")
    #print("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt")
    #print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'""'+" >> Extra.txt")
    #print("sshpass -p 0penBmc ssh root@"+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity"+'"'+" >> Extra.txt")
    print(all52)
    print(allPowerServer[0])
    print(z)
    updateWINTo2(x, z, MeowSP)
    

ipAddr = ""
main_window = None


class ItemSelector(QWidget):
    def __init__(self, items, options_dict, meow_list=None):
        super().__init__()
        self.items = items
        self.options_dict = options_dict
        self.dialogs = {}
        self.meow_list = meow_list or []
        self.setDisabled(False)

        self.layout = QVBoxLayout(self)  # Главный вертикальный layout

        # === Убираем отображение meow_list ===
        self.meow_label = QTextEdit(self)
        self.meow_label.setReadOnly(True)
        self.meow_label.setFixedHeight(100)
        self.meow_label.setStyleSheet("background-color: #f0f0f0; font-family: Consolas;")
        if self.meow_list:
            self.meow_label.setText("\n".join(self.meow_list))
        else:
            self.meow_label.setText("Список пуст или не передан.")
        
        # Убираем meow_label с главного окна
        self.meow_label.setVisible(False)  # Скрыть виджет

        # Остальная часть конструктора
        # === Горизонтальный layout: левая панель + правая таблица ===
        main_h_layout = QHBoxLayout()
        self.layout.addLayout(main_h_layout)

        # Левая часть
        left_split = QVBoxLayout()
        main_h_layout.addLayout(left_split, 1)

        # Список с галочками
        self.list_widget = QListWidget(self)
        for item in self.items:
            list_item = QListWidgetItem(item)

            # Найдём связанный текст из meow_list, где содержится имя item
            related_meow_lines = [
                line for line in self.meow_list
                if item in line
            ]

            # Проверим наличие строки "ERROR : NoData" в найденных строках
            is_meow_error = any("ERROR : NoData" in line for line in related_meow_lines)

            has_data = any(item in values for values in self.options_dict.values())
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)

            if is_meow_error:
                list_item.setFlags(list_item.flags() & ~Qt.ItemIsEnabled)  # Заблокировать
                list_item.setForeground(QColor("red"))
                list_item.setCheckState(Qt.Unchecked)
            elif not has_data:
                list_item.setFlags(list_item.flags() & ~Qt.ItemIsEnabled)
                list_item.setForeground(QColor("red"))
                list_item.setCheckState(Qt.Unchecked)
            else:
                list_item.setCheckState(Qt.Unchecked)

            self.list_widget.addItem(list_item)

        left_split.addWidget(self.list_widget)

        # IP секция
        ip_section = QWidget()
        ip_layout = QVBoxLayout(ip_section)
        ip_layout.setContentsMargins(0, 0, 0, 0)

        self.ip_label = QLabel("Выберите или введите IP-адрес:")
        
        # Создание выпадающего списка для ввода IP-адреса
        self.ip_combo = QComboBox(self)
        self.ip_combo.setPlaceholderText("Например: 192.168.0.10")
        
        # Загрузка IP-адресов из JSON
        self.load_ip_addresses_from_json()

        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Введите новый IP, если его нет в списке.")
        
        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.clicked.connect(self.confirm_ip)

        # Кнопки ВКЛ и ВЫКЛ
        self.buttons_layout = QHBoxLayout()  # Горизонтальный layout для кнопок
        self.green_button = QPushButton("ВКЛ")
        self.red_button = QPushButton("ВЫКЛ")
        self.green_button.setStyleSheet("background-color: green; color: white;")
        self.red_button.setStyleSheet("background-color: red; color: white;")

        

        # Добавляем обработчики нажатий
        self.green_button.clicked.connect(self.turn_on)
        self.red_button.clicked.connect(self.turn_off)

        # Добавляем кнопки в layout
        self.buttons_layout.addWidget(self.green_button)
        self.buttons_layout.addWidget(self.red_button)
        # Добавляем кнопки в layout
        self.buttons_layout.addWidget(self.green_button)
        self.buttons_layout.addWidget(self.red_button)

        


        # Подключение сигнала выбора IP из комбобокса к полю ввода
        self.ip_combo.currentTextChanged.connect(self.update_ip_input_from_combo)

        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_combo)  # Добавляем комбобокс вместо поля ввода
        ip_layout.addWidget(self.ip_input)  # Оставляем поле ввода для новых IP
        ip_layout.addWidget(self.confirm_button)

        # Добавляем кнопки
        ip_layout.addLayout(self.buttons_layout)

        # Размещение в левом разделе (если он есть)
        left_split.addWidget(ip_section)

        # Таблица
        self.main_table = QTableWidget(self)
        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels(["Sensor", "RedFish", "D-Bus", "Ipmitool"])
        font = QFont("Courier New", 10)
        font.setPointSizeF(font.pointSizeF() * 0.8)
        self.main_table.setFont(font)

        main_h_layout.addWidget(self.main_table, 4)

        self.list_widget.itemChanged.connect(self.on_item_changed)

    def load_ip_addresses_from_json(self):
        json_file_name = "ipadr.json"
        try:
            with open(json_file_name, 'r') as f:
                data = json.load(f)
                self.ip_addresses = [item.get('IP') for item in data if 'IP' in item]
                self.ip_combo.addItems(self.ip_addresses)  # Добавляем IP-адреса в комбобокс
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке IP-адресов из файла: {e}")

    def update_ip_input_from_combo(self, text):
        # Автозаполнение поля ввода при выборе IP из списка
        self.ip_input.setText(text)

    def confirm_ip(self):
        global ipAddr
        ipAddr = self.ip_input.text() or self.ip_combo.currentText()  # Берем IP из поля или комбобокса
        
        if not ipAddr:
            ipAddr = "172.26.24.14"  # IP по умолчанию
            self.ip_label.setText(f"IP-адрес не был введён. Используется IP по умолчанию: {ipAddr}")
        else:
            self.ip_label.setText(f"IP-адрес: {ipAddr}")
        # Закрытие всех диалогов, очистка списка диалогов
        for dialog in self.dialogs.values():
            dialog.close()
        self.dialogs.clear()

        # Создание и отображение оверлея 
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
        self.overlay.setGeometry(self.geometry())
        self.overlay.raise_()
        self.overlay.show()
        
        # Отключение основной формы
        self.setDisabled(True)
        
        
        
        # Дополнительная логика, например, вызов функции с IP-адресом
        CatMeow(ipAddr)  # Передача IP в функцию CatMeow

    
    def turn_on(self):
        global ipAddr
        print(f"Включение устройства с IP: {ipAddr}")
        # Замените на вашу команду для включения
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool power on")

    def turn_off(self):
        global ipAddr
        print(f"Выключение устройства с IP: {ipAddr}")
        # Замените на вашу команду для выключения
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool power off")


        


    def show_selected(self, selected_items):
        filtered_options = []
        for key, value in self.options_dict.items():
            if any(selected_item in value for selected_item in selected_items):
                filtered_options.append(key)
        options_text = "\n".join(filtered_options)
        self.update_main_table(options_text)

    def update_main_table(self, options_text):
        self.main_table.clearContents()
        self.main_table.setRowCount(0)
        elements = options_text.split('\n')
        bad_values = {"nan", "null", "0.0", "0.00", "0V", "0W", "0A", "0°C", "0%", "0RPM", "noreading"}
        row = 0

        for element in elements:
            if not element.strip():
                continue

            parts = element.split("!")

            # === Пропускаем строки вида NoData NoData NoDataXXX ===
            if (len(parts) == 3 and parts[0] == "NoData" and parts[1] == "NoData" and
                    parts[2].startswith("NoData") and parts[2][6:].isdigit()):
                continue

            self.main_table.insertRow(row)
            has_bad_value = any(
                parts[col].strip() in bad_values for col in [1, 2, 3] if col < len(parts)
            )

            for col in range(4):
                value = parts[col] if col < len(parts) else ""
                item = QTableWidgetItem(value)

                # 🔴 Отключаем перенос текста в 4-м столбце
                if col == 3:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)
                    self.main_table.setWordWrap(False)
                    
                if col in [1, 2, 3] and value.strip() in bad_values:
                    item.setForeground(QColor("red"))
                if col == 0 and has_bad_value:
                    item.setForeground(QColor(139, 0, 0))

                self.main_table.setItem(row, col, item)


            row += 1

        self.main_table.resizeColumnToContents(3)
        self.main_table.resizeRowsToContents()


    def on_item_changed(self, item):
        selected_items = [self.list_widget.item(i).text()
                          for i in range(self.list_widget.count())
                          if self.list_widget.item(i).checkState() == Qt.Checked]

        if item.checkState() == Qt.Checked:
            self.open_dialog(item.text())
        else:
            self.close_related_dialogs(item.text())

        self.show_selected(selected_items)

    def open_dialog(self, item_text):
        text_to_display = []
        for key, value in self.options_dict.items():
            if item_text in value:
                text_to_display.append(key)
        dialog_text = "\n".join(text_to_display).strip()
        if dialog_text and item_text not in self.dialogs:
            try:
                idx = self.items.index(item_text)
                header_text = self.meow_list[idx] if idx < len(self.meow_list) else ""
            except ValueError:
                header_text = ""
            self.create_dialog(item_text, dialog_text, item_text, header_text)


    def close_related_dialogs(self, item_text):
        if item_text in self.dialogs:
            self.dialogs[item_text].close()
            del self.dialogs[item_text]

    def create_dialog(self, title, text, item_text, header_text=""):
        dialog = QDialog(self)
        
        if "Server_Board" in title or "Server_Board" == title:
            title = "AQC621AB Motherboard"
        dialog.setWindowTitle(title)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(10, 10, 10, 10)

        header_table = None
        header_table_height = 0
        header_table_width = 0

        if header_text.strip():
            header_table = QTableWidget()
            header_table.setColumnCount(2)
            header_table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            header_table.verticalHeader().setVisible(False)
            header_table.setEditTriggers(QTableWidget.NoEditTriggers)
            header_table.setSelectionMode(QTableWidget.NoSelection)
            header_table.setWordWrap(True)  # уже есть — отлично
            header_table.resizeColumnsToContents()  # ок
            header_table.resizeRowsToContents()

            font = QFont("Segoe UI", 10)
            header_table.setFont(font)

            rows = [line for line in header_text.strip().split('\n') if ':' in line]

            # Проверка на особый случай: одна строка и ERROR: NoData
            if len(rows) == 1:
                key, value = map(str.strip, rows[0].split(':', 1))
                if key.upper() == "ERROR" and value == "NoData":
                    header_table.setRowCount(1)
                    item = QTableWidgetItem("Отсутствует информация по плате")
                    item.setFont(font)
                    item.setForeground(QColor("red"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsEnabled)
                    header_table.setSpan(0, 0, 1, 2)
                    header_table.setItem(0, 0, item)
                else:
                    header_table.setRowCount(1)
                    key_item = QTableWidgetItem(key)
                    value_item = QTableWidgetItem(value)

                    key_item.setForeground(QColor("#003366"))
                    value_item.setForeground(QColor("#333333"))

                    key_item.setFont(font)
                    value_item.setFont(font)

                    key_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
                    value_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)

                    key_item.setFlags(Qt.ItemIsEnabled)
                    value_item.setFlags(Qt.ItemIsEnabled)

                    header_table.setItem(0, 0, key_item)
                    header_table.setItem(0, 1, value_item)
            else:
                header_table.setRowCount(len(rows))
                for i, line in enumerate(rows):
                    key, value = map(str.strip, line.split(':', 1))
                    key_item = QTableWidgetItem(key)
                    value_item = QTableWidgetItem(value)

                    key_item.setForeground(QColor("#003366"))
                    value_item.setForeground(QColor("#333333"))

                    key_item.setFont(font)
                    value_item.setFont(font)

                    key_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
                    value_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)

                    key_item.setFlags(Qt.ItemIsEnabled)
                    value_item.setFlags(Qt.ItemIsEnabled)

                    header_table.setItem(i, 0, key_item)
                    header_table.setItem(i, 1, value_item)

            header_table.resizeColumnsToContents()
            header_table.resizeRowsToContents()

            for row in range(header_table.rowCount()):
                header_table.setRowHeight(row, max(30, header_table.rowHeight(row)))

            header_table.setStyleSheet("""
                QTableWidget {
                    background-color: #f8faff;
                    border: 1px solid #ccd;
                    font-size: 10pt;
                }
            """)

            header_table_width = header_table.verticalHeader().width()
            for col in range(header_table.columnCount()):
                header_table_width += header_table.columnWidth(col)

            header_table_height = header_table.horizontalHeader().height()
            for row in range(header_table.rowCount()):
                header_table_height += header_table.rowHeight(row)

            MAX_HEADER_HEIGHT = 1000
            EXTRA_PADDING = 10

            scroll_header = QScrollArea()
            scroll_header.setWidgetResizable(True)
            scroll_header.setFrameShape(QFrame.NoFrame)
            scroll_header.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll_header.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_header.setWidget(header_table)

            if header_table_height + EXTRA_PADDING <= MAX_HEADER_HEIGHT:
                scroll_header.setFixedHeight(header_table_height + EXTRA_PADDING)
            else:
                scroll_header.setFixedHeight(MAX_HEADER_HEIGHT)

            visible_header_height = scroll_header.height()
            layout.addWidget(scroll_header)

        sensor_table = QTableWidget()
        sensor_table.setColumnCount(4)
        sensor_table.setHorizontalHeaderLabels(["Sensor", "RedFish", "D-Bus", "Ipmitool"])

        sensor_font = QFont("Courier New", 9)
        sensor_table.setFont(sensor_font)

        sensor_table_height = 0
        sensor_table_width = 0

        bad_values = {"nan", "null", "0.0", "0.00", "0V", "0W", "0A", "0°C", "0%", "0RPM", "noreading"}
        elements = text.split('\n')

        valid_elements = []
        meow_line_detected = False
        meow_candidate = None

        for element in elements:
            parts = element.strip().split("!")
            if len(parts) == 3 and parts[0] == "NoData" and parts[1] == "NoData" and parts[2].startswith("NoData") and parts[2][6:].isdigit():
                meow_line_detected = True
                meow_candidate = element.strip()
                continue
            if element.strip():
                valid_elements.append(element.strip())

        if meow_line_detected and len(valid_elements) == 0:
            valid_elements.append("__MEOW__")

        row_index = 0
        for element in valid_elements:
            if element == "__MEOW__":
                sensor_table.insertRow(row_index)
                item = QTableWidgetItem("Отсутствует информация по сенсорам")
                item.setForeground(QColor("red"))
                item.setFont(sensor_font)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsEnabled)
                sensor_table.setSpan(row_index, 0, 1, 4)
                sensor_table.setItem(row_index, 0, item)
                row_index += 1
                continue
            
            parts = element.split("!")
            sensor_table.insertRow(row_index)
            has_bad = any(parts[col].strip() in bad_values for col in [1, 2, 3] if col < len(parts))

            for col_index in range(4):
                value = parts[col_index] if col_index < len(parts) else ""
                item = QTableWidgetItem(value)

                if col_index in [1, 2, 3] and value.strip() in bad_values:
                    item.setForeground(QColor("red"))
                if col_index == 0 and any(parts[c].strip() in bad_values for c in [1, 2, 3] if c < len(parts)):
                    item.setForeground(QColor(139, 0, 0))

                item.setFont(sensor_font)
                sensor_table.setItem(row_index, col_index, item)

            row_index += 1

        sensor_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sensor_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        sensor_table.setFrameShape(QFrame.NoFrame)

        sensor_table.setColumnWidth(0, 100)
        sensor_table.resizeColumnsToContents()
        sensor_table.resizeRowsToContents()

        sensor_table_width = sensor_table.verticalHeader().width()
        for col in range(sensor_table.columnCount()):
            sensor_table_width += sensor_table.columnWidth(col)

        sensor_table_height = sensor_table.horizontalHeader().height()
        qws = 0
        for row in range(sensor_table.rowCount()):
            sensor_table_height += sensor_table.rowHeight(row)
            qws = qws + 1
            if qws <= 2:
                remove_scrollbar = True

            

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(sensor_table)
        if remove_scrollbar:
                #sensor_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        max_height = 1000
        total_height = header_table_height + sensor_table_height
        final_height = min(total_height, max_height)

        total_width = max(sensor_table_width, header_table_width) + 40

        if total_height > max_height:
            scroll_bar_width = QApplication.style().pixelMetric(QStyle.PM_ScrollBarExtent)
            total_width += scroll_bar_width

        scroll.setMinimumSize(total_width, final_height - header_table_height)
        dialog.resize(total_width, final_height - 200)

        self.dialogs[item_text] = dialog
        dialog.setWindowModality(Qt.NonModal)
        dialog.show()





    def enable_overlay(self):
        if hasattr(self, 'overlay') and self.overlay:
            self.overlay.show()
        else:
            self.overlay = QWidget(self)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
            self.overlay.setGeometry(self.rect())
            self.overlay.raise_()
            self.overlay.show()

    def disable_overlay(self):
        if hasattr(self, 'overlay') and self.overlay:
            self.overlay.hide()




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Состав оборудования")
        self.setGeometry(0, 0, 1920, 1280)
        self.setFixedSize(1920, 1280)

        self.layout = QVBoxLayout(self)
        self.stack = QStackedLayout()
        self.layout.addLayout(self.stack)

        self.page1 = QWidget()
        p1_layout = QVBoxLayout(self.page1)
        self.label = QLabel("Ожидается ввод IP.")
        p1_layout.addWidget(self.label)

        self.stack.addWidget(self.page1)
        self.page2 = None

        self.show()

        QTimer.singleShot(100, self.get_ip_address)

    def get_ip_address(self):
        global ipAddr

        # Загружаем IP-адреса из файла ipadr.json
        with open('ipadr.json', 'r') as file:
            ip_data = json.load(file)

        # Создаем кастомный диалог
        dialog = QDialog(self)
        dialog.setWindowTitle("Введите IP-адрес")
        dialog.setMinimumSize(500, 250)  # Устанавливаем размер диалога

        # Основной layout для диалога
        layout = QVBoxLayout(dialog)

        # Создаем поле ввода для IP-адреса
        ip_input = QLineEdit(dialog)
        layout.addWidget(ip_input)

        # Создаем выпадающий список для IP-адресов и добавляем текст для выбора
        ip_combo = QComboBox(dialog)
        ip_combo.addItem("Выбрать IP")  # Добавляем текст "Выбрать IP" как первый элемент
        for entry in ip_data:
            ip_combo.addItem(entry["IP"])
        layout.addWidget(ip_combo)

        # Обработчик изменения выбранного IP
        ip_combo.currentIndexChanged.connect(lambda: ip_input.setText(ip_combo.currentText() if ip_combo.currentIndex() > 0 else ""))

        # Создаем кнопки ВКЛ/ВЫКЛ
        buttons_layout = QHBoxLayout()  # Горизонтальный layout для кнопок
        self.green_button = QPushButton("ВКЛ")
        self.red_button = QPushButton("ВЫКЛ")
        self.green_button.setStyleSheet("background-color: green; color: white;")
        self.red_button.setStyleSheet("background-color: red; color: white;")
        
        # Изначально кнопки выключены
        self.green_button.setEnabled(False)
        self.red_button.setEnabled(False)

        # Добавляем обработчики нажатий
        self.green_button.clicked.connect(lambda: self.turn_on(ip_input.text()))
        self.red_button.clicked.connect(lambda: self.turn_off(ip_input.text()))

        # Добавляем кнопки в layout
        buttons_layout.addWidget(self.green_button)
        buttons_layout.addWidget(self.red_button)

        # Добавляем кнопки в основной layout диалога
        layout.addLayout(buttons_layout)

        # Создаем кнопку OK
        ok_button = QPushButton("OK", dialog)
        layout.addWidget(ok_button)

        # Обработчик нажатия на кнопку OK
        ok_button.clicked.connect(lambda: self.on_ok_pressed(ip_input.text(), ip_combo.currentText(), dialog))

        # Обработчик на изменение текста в поле ввода IP
        ip_input.textChanged.connect(lambda: self.update_buttons(ip_input.text()))

        dialog.exec_()  # Показываем диалог

    def on_ok_pressed(self, ip_input_value, ip_combo_value, dialog):
        global ipAddr
        dialog.accept()  # Закрываем диалог

        # Проверяем, что пользователь ввел IP в текстовое поле или выбрал из выпадающего списка
        if ip_input_value.strip():  # Если IP введен в текстовое поле
            ipAddr = ip_input_value
        elif ip_combo_value.strip() and ip_combo_value != "Выбрать IP":  # Если IP выбран из выпадающего списка, игнорируя "Выбрать IP"
            ipAddr = ip_combo_value
        else:
            ipAddr = "172.26.24.14"  # IP по умолчанию, если ничего не введено

        self.label.setText(f"Используется IP: {ipAddr}")  # Обновляем метку с выбранным IP
        CatMeow(ipAddr)  # Вызываем функцию с выбранным IP

    def update_buttons(self, ip_input_value):
        # Если поле ввода IP не пустое, активируем кнопки
        if ip_input_value.strip():
            self.green_button.setEnabled(True)
            self.red_button.setEnabled(True)
        else:
            self.green_button.setEnabled(False)
            self.red_button.setEnabled(False)

    def turn_on(self, ip_input_value):
        global ipAddr
        ipAddr = ip_input_value.strip() if ip_input_value.strip() else "172.26.24.14"
        print("Выключение устройства")
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool power on")

    def turn_off(self, ip_input_value):
        global ipAddr
        ipAddr = ip_input_value.strip() if ip_input_value.strip() else "172.26.24.14"
        print("Выключение устройства")
        os.system("sshpass -p 0penBmc ssh root@"+ipAddr+" ipmitool power off")

    def updateWINTo2(self, x, y, meow_list=None):
        if self.page2:
            self.stack.removeWidget(self.page2)
            self.page2.deleteLater()

        self.page2 = ItemSelector(x, y, meow_list)
        self.stack.addWidget(self.page2)
        self.stack.setCurrentWidget(self.page2)

    def closeEvent(self, event):
        print("Закрытие приложения и всех окон.")
        QApplication.quit()



def updateWINTo2(x, z, meow_list=None):
    if main_window:
        main_window.updateWINTo2(x, z, meow_list)
# === Глобальные переменные ===
overlay_widget = None
progress_overlay = None
progress_dots = []
progress_labels = []
progress_bar = None
main_window = None  # <- должен быть определён в __main__


def MeowOn():
    """
    Показывает затемнение с 7 точками, подписями и прогресс-баром.
    Подписи берутся из массива внутри этой функции.
    """
    global overlay_widget, progress_overlay, progress_dots, progress_labels, progress_bar, main_window

    if not main_window:
        print("❌ main_window is not set.")
        return

    # Сбросим всё, если уже было
    MeowOff()

    # === Встроенный массив подписей ===
    progress_texts = ["Очистка Системы", "Получение названий плат", "Получиние деревьев BUCSTL", "Получение информации по BUCSTL", "Получение информации по RedFish", "Создание общего списка", "Передача данных в интерфейс"]

    # Создаём затемнение
    overlay_widget = QWidget(main_window)
    overlay_widget.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
    overlay_widget.setGeometry(main_window.rect())
    overlay_widget.setAttribute(Qt.WA_DeleteOnClose)
    overlay_widget.show()

    # Контейнер поверх затемнения
    progress_overlay = QWidget(overlay_widget)
    progress_overlay.setGeometry(0, 0, overlay_widget.width(), overlay_widget.height())
    progress_overlay.setStyleSheet("background: transparent;")

    layout = QVBoxLayout(progress_overlay)
    layout.setAlignment(Qt.AlignCenter)

    container = QWidget()
    container.setFixedWidth(1300)
    inner_layout = QVBoxLayout(container)
    #inner_layout.setSpacing(20)
    #inner_layout.setAlignment(Qt.AlignTop)

    # Точки и подписи
    progress_dots = []
    progress_labels = []

    for i in range(7):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignLeft)
        row.setSpacing(15)  # ⬅️ Отступ между точкой и текстом

        dot = QLabel("●")
        dot.setFont(QFont("Arial", 18, QFont.Bold))  # ⬅️ Размер и жирность точки
        dot.setStyleSheet("color: gray;")
        progress_dots.append(dot)

        label = QLabel(progress_texts[i])
        label.setFont(QFont("Segoe UI", 10))  # ⬅️ Шрифт текста
        label.setStyleSheet("color: white;")
        progress_labels.append(label)

        row.addWidget(dot)
        row.addWidget(label)
        inner_layout.addLayout(row)


    # Прогресс-бар
    progress_bar = QProgressBar()
    
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(7)
    progress_bar.setValue(0)
    progress_bar.setStyleSheet("""
        QProgressBar {
            background-color: #444;
            color: white;
            border: 1px solid #aaa;
            height: 20px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: limegreen;
        }
    """)

    inner_layout.addSpacing(30)
    inner_layout.addWidget(progress_bar)
    layout.addWidget(container)

    progress_overlay.show()
    overlay_widget.raise_()



def ProgressMeow(j):
    """
    Обновляет точки и прогресс-бар в зависимости от переданного j
    """
    global progress_dots, progress_bar

    for i, dot in enumerate(progress_dots):
        if i < j:
            dot.setStyleSheet("color: limegreen;")
        else:
            dot.setStyleSheet("color: gray;")

    if progress_bar:
        progress_bar.setValue(j)
    def animate_progress_bar(to_value, duration=500):
        global progress_bar
        if not progress_bar:
            return

        animation = QPropertyAnimation(progress_bar, b"value")
        animation.setDuration(duration)  # длительность анимации в мс
        animation.setStartValue(progress_bar.value())
        animation.setEndValue(to_value)
        animation.start(QPropertyAnimation.DeleteWhenStopped)


def MeowOff():
    """
    Закрывает затемнение и очищает прогресс-интерфейс
    """
    global overlay_widget, progress_overlay, progress_dots, progress_labels, progress_bar

    if overlay_widget:
        overlay_widget.close()
        overlay_widget = None

    progress_overlay = None
    progress_dots = []
    progress_labels = []
    progress_bar = None





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    sys.exit(app.exec_())
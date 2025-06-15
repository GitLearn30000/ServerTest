import datetime
import os
import sys
import math
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ipmi import GetIpmiData
from busctl import GetBusctlData
from redfish import GetRedfishData
from IDandToken import GetIDandToken
import re
#10.12.140.137

sshConnectionString = "sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"
scpConnectionString = "sshpass -p 0penBmc scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"
def StartProgramm(ipAddr):
    for filename in ["CBA.txt", "ABC.txt","Sdr.txt", "PowerServer.txt"]:
        if os.path.exists(filename):
            os.remove(filename)
            print("")#print(f"✅ Удалено: {filename}")
        else:
            print("")#print(f"❌ Не найдено: {filename}")
    os.system(sshConnectionString+ipAddr+" ipmitool power status"+" > PowerServer.txt")
    os.system(scpConnectionString+ipAddr+":/home/root/PowerServer.txt ./")
    TrueID, TrueToken = GetIDandToken(ipAddr)
    print("Получено из фунцкии: ",TrueID, TrueToken)
    with open("PowerServer.txt", "r") as filePowerServer: #чтение файла с данными на пользовательской стороне
        contentPowerServer = filePowerServer.read()
        print("")#print(contentPowerServer)
            
        
        PowerServer82 = '\n'.join(line + '!' for line in contentPowerServer.splitlines())
        allPowerServer = PowerServer82.split(("!"))
    print("")#print(allPowerServer[0])

    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #тут редактировать обработку Json для RedFish
    
    # Загрузка данных из файла paths.json
    with open('paths.json', 'r', encoding='utf-8') as file:
        GetDataFromFile = json.load(file)

    # Инициализация пустых списков для хранения значений
    RedFishQwery_SP = []
    SensorNames = []
    DBusQwery_SP = []
    StateServer = []
    serverstate = ""
    if "is on" in allPowerServer[0]:
        serverstate = "on"
    else:
        serverstate = "off"
    # Переменная состояния сервера
    stateMyServer = serverstate  # Замените на "on" для тестирования другого состояния

    # Функция для рекурсивного поиска значений
    def FilePathsData(current_data):
        if isinstance(current_data, dict):
            # Проверяем наличие нужных ключей в самом словаре
            if "PowerState" in current_data:
                power_state = current_data["PowerState"]
                if stateMyServer == "off" and power_state == "off":
                    add_values(current_data)  # Добавляем только данные с PowerState "off"
                elif stateMyServer == "on":
                    add_values(current_data)  # Добавляем все данные при "on"
            else:
                # Если ключа "PowerState" нет, продолжаем рекурсивный вызов
                for keyData, ValueData in current_data.items():
                    FilePathsData(ValueData)
        elif isinstance(current_data, list):
            for itemData in current_data:
                FilePathsData(itemData)

    # Функция для добавления значений в списки
    def add_values(data):
        if "redfishPath" in data:
            RedFishQwery_SP.append(data["redfishPath"])
        if "sensorName" in data:
            SensorNames.append(data["sensorName"])
        if "dbusPath" in data:
            DBusQwery_SP.append(data["dbusPath"])
        if "PowerState" in data:
            StateServer.append(data["PowerState"])

    # Начало извлечения
    FilePathsData(GetDataFromFile)

    # Вывод результата
    print("")#print("redfishPath values:", RedFishQwery_SP, len(RedFishQwery_SP))
    print("")#print("sensorName values:", SensorNames, len(SensorNames))
    print("")#print("dbusPath values:", DBusQwery_SP, len(DBusQwery_SP))
    print("")#print("PowerState values:", StateServer, len(StateServer))

    # Если вам нужно сохранить все значения redfishPath в переменной all5
    all5 = RedFishQwery_SP
    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    ProgressbarSrceenON()
    ProgressbarState(1)
    SENSOR_NAME_LIST = SensorNames
    end_dict = {}
    CurlRequest = "curl -k -u root:0penBmc -L https://"
    def GetFirmwareVersions(ipAddr):
        a = datetime.datetime.now()
        os.system(CurlRequest+ipAddr+"/redfish/v1/Managers/bmc | grep FirmwareVersion > informationversion.txt")
        os.system(CurlRequest+ipAddr+"/redfish/v1/Systems/system | grep BiosVersion >> informationversion.txt")
        os.system(CurlRequest+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem/Aquarius_Irteya/HeatingUnit  | grep FirmwareVersion >> informationversion.txt")
        
        with open("informationversion.txt", "r") as informationfile: #чтение файла с данными на серверной стороне
            informationType = informationfile.read()
            print("")#print(informationType)
            #informationSTR = '\n'.join(line + '!' for line in informationType.splitlines())
            information_SP = informationType.split(("\n"))
        print("")#print(information_SP)
        b = datetime.datetime.now()
        print("")#print("Time difference for getting GetFirmwareVersions = ", b -a)
        return information_SP
    
    def HU_GetInfo():
        a = datetime.datetime.now()
        Qwery1 = '''curl -s -k -u root:0penBmc -X GET "https://172.26.24.21/redfish/v1/Chassis/IR_AX_HU_Board/Oem/Aquarius_Irteya/HeatingUnit" | jq '.Temperatures,.FirmwareVersion,.Humidity' '''
        Qwery2 = '''sshpass -p 0penBmc ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@172.26.24.21 'busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "Temperatures\|Humidity " && exit' '''
        result2 = os.popen(Qwery1).read()
        result3 = os.popen(Qwery2).read()

        
        result2_1=result2.split("]")
        result2_1_1=result2_1[0]
        result2_1_1=result2_1_1.replace("[\n","")
        while " " in result2_1_1:
            result2_1_1=result2_1_1.replace(" ","")
        while "," in result2_1_1:
            result2_1_1=result2_1_1.replace(",","")
        result2_1_1=result2_1_1.split("\n")
        result_222 = []
        for i0 in result2_1_1:
            if len(i0) >= 2:
                if i0 != "null":
                    number = float(i0)
                    i0 = f"{number:.2f}"
                    result_222=result_222+[i0]
                if i0 == "null":
                    result_222=result_222+["null"]


        
        
        result2_1_2=result2_1[1]
        result2_1_2=result2_1_2.split('"')
        result2_1_2=result2_1_2[len(result2_1_2)-1]
        result2_1_2=result2_1_2.replace("\n","")
        number = float(result2_1_2)
        result2_1_2 = f"{number:.2f}"

        result3=result3.replace(".Humidity","")
        result3=result3.replace(".Temperatures","")
        result3=result3.replace("emits-change","",10)
        result3=result3.replace("property  d","",10)
        result3=result3.replace("property","",10)
        result3=result3.replace("\n","",10)
        result3=result3.split("ad")
        result3_1=result3[0]
        result3_1=result3_1.split(" ")
        Res3_1=""
        for i1 in result3_1:
            if len(i1) >= 4:
                number = float(i1)
                i1 = f"{number:.2f}"
                Res3_1 = i1
        result3_2=result3[1]
        result3_2=result3_2.split(" ")
        print("Result3_2 ", result3_2)
        Res3_2=[]
        for i2 in result3_2:
            
            if len(i2) >= 2:
                if i2 != "nan":
                    number = float(i2)
                    i2 = f"{number:.2f}"
                    Res3_2 = Res3_2 + [i2]
                if i2 == "nan":
                    Res3_2 = Res3_2 + ["nan"]

        #print("Result2 ", result2)
        #print("Result3 ", result3)
        print("Result2-1 ", result_222)
        print("Result2-2 ", result2_1_2)
        print("Result3_1 ", Res3_1)
        print("Result3_2 ", Res3_2)
        end_dict = {}
        end_dict["HEATER_HUMID-0!"+result2_1_2+"!"+Res3_1+"!-"]="IR-AX-HU"
        
        s = [0,1,2,3,4,5,6]
        for i in s:
            i = int(i)
            print(str("HEATER_TEMP-"+str(i)+"!"+result_222[i]+"!"+Res3_2[i])+"!-")
            end_dict[str("HEATER_TEMP-"+str(i)+"!"+result_222[i]+"!"+Res3_2[i])+"!-"]="IR-AX-HU"+str(i)
        
        print("End_dict:  ",end_dict)
        



        #os.system("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 > Extra.txt && echo ------- >> Extra.txt")
        #os.system(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        #os.system("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'\\'+'""'+" >> Extra.txt && echo ------- >> Extra.txt")
        #os.system(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity "+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
        #os.system(scpConnectionString+ipAddr+":/home/root/Extra.txt ./")
        
        
        return end_dict
    #ProgressbarState(0)
    
    os.system(sshConnectionString+ipAddr+" 'rm Extra.txt'")
    
    #ipmitool sdr

    def BoardNames():
        a = datetime.datetime.now()
        os.system(sshConnectionString+ipAddr+" ipmitool fru | grep "+'"'+"FRU Device Description"+'"'+" > BoardNamesList.txt") #ipmitool fru | grep "FRU Device Description"> BoardNamesList.txt
        os.system(scpConnectionString+ipAddr+":/home/root/BoardNamesList.txt ./")
        with open("BoardNamesList.txt", "r") as FileBoardNamesList: #чтение файла с данными на пользовательской стороне
            FileDataBoardNamesList = FileBoardNamesList.read()
            print("")#print(FileDataBoardNamesList)
                
            FileDataBoardNames_SP = '\n'.join(line + '!' for line in FileDataBoardNamesList.splitlines())
            FileDataPlates = FileDataBoardNames_SP.split(("!"))
        print("")#print(FileDataPlates)
        #busctl introspect xyz.openbmc_project.FruDevice /xyz/openbmc_project/FruDevice/AQC621AB
        
        FixBoardsNames = []
        for FileDataPlate in FileDataPlates:
            TempDataPlate = FileDataPlate.replace("FRU Device Description : ","")
            
            SplitFileDataPlate = TempDataPlate.split("(")
            DataPlate=SplitFileDataPlate[0]
            DataPlate = DataPlate.replace(" ","")
            DataPlate = DataPlate.replace("\n","")
            if DataPlate != "":
                DataPlate=DataPlate.replace("BuiltinFRUDevice","AQUARIUS_AQC621AB")
                DataPlate=DataPlate.replace("AQFPB-FFC","AQFPB_FFC")#AQRZ2_U4P1_R_TMP
                DataPlate=DataPlate.replace("AQRZ2-U4P1-R","AQRZ2_U4P1_R")
                FixBoardsNames = FixBoardsNames + [DataPlate]
        selected_items = FixBoardsNames
        b = datetime.datetime.now()
        print("")#print("Time difference for getting BoardNames = ", b -a)
        return selected_items,FixBoardsNames
    
        #FixBoardsNames = FixBoardsNames + ["AQUARIUS_AQC621AB"]
    def GetBoardsDATA():
        a = datetime.datetime.now()
        os.system(sshConnectionString+ipAddr+" ipmitool fru > BoardsDATA.txt") #ipmitool fru | grep "FRU Device Description"> BoardNamesList.txt
        os.system(scpConnectionString+ipAddr+":/home/root/BoardsDATA.txt ./")
        #FixBoardsNames = FixBoardsNames +  ["Server_Chassis"]
        with open("BoardsDATA.txt", "r") as BoardsDATAFileStr: #чтение файла с данными на пользовательской стороне
            BoardsDATAFixValue= BoardsDATAFileStr.read()
            print("")#print(BoardsDATAFixValue)
            BoardsDATAFixValue=BoardsDATAFixValue.replace("Product Area Checksum : OK","") 
            BoardsDATAFixValue=BoardsDATAFixValue.replace("Chassis Area Checksum : OK","")      
            BoardsDATAFixValue=BoardsDATAFixValue.replace("Board Area Checksum   : OK","")
            BoardsDATAFixValue=BoardsDATAFixValue.replace("Product Asset Tag     : asset_tag_vv","")
            BoardsDATAFixValue=BoardsDATAFixValue.replace("Device not present (Requested sensor, data, or record not found)","ERROR : NoData")
            #Device not present (Requested sensor, data, or record not found)
            FinalBoardsData_SP = '\n'.join(line + '!' for line in BoardsDATAFixValue.splitlines())
            
            FileDataWithExtra = FinalBoardsData_SP.split(("FRU Device Description :"))
        print("")#print(FileDataWithExtra)
        
        BoardsDataList = []
        DeleteExtraBoard = ""
        
        for BoardNameCheck in FileDataWithExtra:
            
            
            if "BuiltinFRUDevice" not in BoardNameCheck:
                while "!" in BoardNameCheck:
                    BoardNameCheck = BoardNameCheck.replace("!","")
            if "BuiltinFRUDevice" in BoardNameCheck:
                while "!" in BoardNameCheck:
                    BoardNameCheck = BoardNameCheck.replace("!","")
                DeleteExtraBoard = BoardNameCheck
            if "" != BoardNameCheck:
                BoardsDataList = BoardsDataList + [BoardNameCheck]
                
        BoardsDataList = BoardsDataList + [DeleteExtraBoard]
        #ipAddr = "10.12.140.137"
        print("")#print(BoardsDataList)
        b = datetime.datetime.now()
        print("")#print("Time difference for getting GetBoardsDATA = ", b -a)
        
        return FileDataWithExtra,BoardsDataList
    
    #exit()
    print("")#print("0")
    
    #all5 = ['/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_A_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_A_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_E_TMP','/Chassis/SILICOM_Pomona_Lake_1/Sensors/temperature_SIL_ACC100_W_TMP','/Chassis/AQUARIUS_AQC621AB_Chassis/PowerSubsystem/PowerSupplies/ASPOWER_1600W_PSU_1', '/Chassis/AQUARIUS_AQC621AB_Chassis/PowerSubsystem/PowerSupplies/ASPOWER_1600W_PSU_2', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU1_IN_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU1_OUT_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU2_IN_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/current_PSU2_OUT_AMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_PSU1_FAN_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_PSU2_FAN_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN1_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN2_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN5_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fanpwm_SYS_FAN6_PWM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_PSU1_FAN_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_PSU2_FAN_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN1_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN2_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN5_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/fantach_SYS_FAN6_RPM', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU1_IN_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU1_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU2_IN_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/power_PSU2_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/temperature_PSU1_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/temperature_PSU2_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU1_IN_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU1_OUT_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU2_IN_VLT', '/Chassis/AQUARIUS_AQC621AB_Chassis/Sensors/voltage_PSU2_OUT_VLT', '/Chassis/AQFPB_FFC/Sensors/temperature_AQFPB_FFC_TMP', '/Chassis/AQRZ2_U4P1_R/Sensors/temperature_AQRZ2_U4P1_R_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/power_PSU_TTL_OUT_PWR', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_DTS_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_P1V8_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_PVCCIN_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_CPU1_PVCCIO_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_B_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_C_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_D_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_E_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_F_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_G_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_DDR4_H_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_PVDDQ_ABCD_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_PVDDQ_EFGH_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_TEMP1_OUT_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/temperature_TEMP2_IN_TMP', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_3V_BAT_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_P1V8_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCANA_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCIN_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCIO_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_CPU1_PVCCSA_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P12V_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P1V05_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P1V8_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_P3V3_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVDDQ_ABCD_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVDDQ_EFGH_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVNN_PCH_AX_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVPP_ABCD_VLT', '/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors/voltage_PVPP_EFGH_VLT', '/Chassis/P425G410G8TS81_XR_Silicom_STS4/Sensors/temperature_SIL_STS4_TMP']
    # Загрузка данных из файла paths.json
    
    
    
    
    def run_all_functions(ipAddr):
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(GetFirmwareVersions,ipAddr): 'GetFirmwareVersions',
                executor.submit(GetRedfishData,TrueID, TrueToken,ipAddr,SENSOR_NAME_LIST,all5): 'GetRedfishData',
                executor.submit(GetBusctlData,DBusQwery_SP,ipAddr): 'GetBusctlData',
                executor.submit(BoardNames): 'BoardNames',
                executor.submit(GetBoardsDATA): 'GetBoardsDATA',
                executor.submit(GetIpmiData, ipAddr): 'GetIpmiData',
                executor.submit(HU_GetInfo): 'HU_GetInfo',
                
            }

            results = {}
            for future in as_completed(futures):
                func_name = futures[future]
                try:
                    results[func_name] = future.result()
                except Exception as e:
                    print("")#print(f"{func_name} вызвала исключение: {e}")
        
        # Распаковка результатов
        all52, RedFishList = results['GetRedfishData']
        all59 = results['GetBusctlData']
        selected_items,FixBoardsNames = results['BoardNames']
        FileDataWithExtra, BoardsDataList = results['GetBoardsDATA']
        cSDR, allSDR = results['GetIpmiData']
        end_dict = results['HU_GetInfo']
        information_SP = results['GetFirmwareVersions']

        return all52, RedFishList, all59, FixBoardsNames, selected_items, FileDataWithExtra, BoardsDataList, cSDR, allSDR, end_dict, information_SP

    # Вызов
    all52, RedFishList, all59, FixBoardsNames, selected_items, FileDataWithExtra, BoardsDataList, cSDR, allSDR, end_dict, information_SP = run_all_functions(ipAddr)
    
    
    dub = []
    
    
    DebugList = []
    
    print(all52,"lenAll52: " ,len(all52))
    print(all59,"lenAll59: " ,len(all59))
    print(cSDR)
    print(len(cSDR))
    for i in range(0,len(all59)): #сравнение данных и вывод на экран
        name =SENSOR_NAME_LIST[i]

        print(all52[i],all59[i])
        print(name)
        print(i)
        
        ClienT = all52[i].split(":")
        ClienT = ClienT[1]
        ClienT = ClienT[:-1]
        SerVer1 = all59[i].split(" ")
        SerVer2 = SerVer1[1]
        ert = 0
        #AQRZ2_U4P1_R_TMP
        Redfish_Link = RedFishList[i]
        MQ = RedFishList[i]
        
        
        if "ACC100" in Redfish_Link or "SIL_STS4" in Redfish_Link:
            Redfish_Link = Redfish_Link + "https:///redfish/v1/Chassis/AQUARIUS_AQC621AB_Baseboard/Sensors"
        DebugList = DebugList + [SENSOR_NAME_LIST[i]]
        
            
        

        if ert == 0:
            if ert == 0:
                if ert == 0:
                    if ert == 0:
                        if ert == 0:
                            if ert == 0:
                                if ert == 0:
                                    for SDRvalue in cSDR:
                                        if name in SDRvalue:
                                            if ert == 0:
                                                print("")#print(i)
                                                #print("")#print(len(all52))
                                                #print("")#print(len(all59))
                                                
                                                
                                                

                                                SDRvalue=SDRvalue.replace("\n","")
                                                SDRvalue=SDRvalue.replace(str(SensorNames[i]+"|"),"")
                                                SDRvalue=SDRvalue.replace(str("degreesC"),"°C")
                                                SDRvalue=SDRvalue.replace(str("Volts"),"V")#percent
                                                SDRvalue=SDRvalue.replace(str("percent"),"%")
                                                SDRvalue=SDRvalue.replace(str("Watts"),"W")
                                                SDRvalue=SDRvalue.replace(str("Amps"),"A")
                                                SDRvalue=SDRvalue.replace(str("RPM")," RPM")
                                                BoardValue = Redfish_Link
                                                BoardValue=BoardValue.replace("AQUARIUS_AQC621AB_Chassis","")
                                                BoardValue=BoardValue.replace("AQUARIUS_AQC621AB_Baseboard","")#SIL_STS4
                                                #BoardValue=BoardValue.replace("AQFPB_FFC"," AQFPB-FFC ")
                                                #BoardValue=BoardValue.replace("AQRZ2_U4P1_R_TMP","AQRZ2_U4P1_R")
                                                BoardValue=BoardValue.replace("SIL_STS4","Server_Chassis")#SIL_STS4_TMP
                                                BoardValue=BoardValue.replace("SYS_FAN1_RPM","Server_Chassis")#AQRZ2_U4P1_R_TMP
                                                BoardValue=BoardValue.replace("SYS_FAN2_PWM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN1_PWM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN6_PWM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN5_RPM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN6_RPM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN5_PWM","Server_Chassis")
                                                BoardValue=BoardValue.replace("SYS_FAN2_RPM","Server_Chassis")
                                                BoardValue=BoardValue.replace("ACC100_A_TMP","1Server_Chassis1")
                                                BoardValue=BoardValue.replace("ACC100_E_TMP","2Server_Chassis2")
                                                BoardValue=BoardValue.replace("ACC100_W_TMP","3Server_Chassis3")
                                                BoardValue=BoardValue.replace("PSU_TTL_OUT_PWR","Server_Chassis")
                                                BoardValue=BoardValue.replace("PVPP_ABCD_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVNN_PCH_AX_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVDDQ_ABCD_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_A_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_B_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_F_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_C_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_H_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVDDQ_EFGH_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCIO_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("P1V8_PCH_AX_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("3V_BAT_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("P12V_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCANA_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("TEMP1_OUT_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCIN_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCIO_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVDDQ_EFGH_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_P1V8_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVDDQ_ABCD_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_G_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("P1V05_PCH_AX_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("PVPP_EFGH_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCIN_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_D_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_DTS_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("DDR4_E_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_PVCCSA_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("P3V3_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("CPU1_P1V8_VLT"," Server_Board ")
                                                BoardValue=BoardValue.replace("TEMP2_IN_TMP"," Server_Board ")
                                                BoardValue=BoardValue.replace("PSU1_IN_VLT","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_OUT_PWR","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_OUT_VLT","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_IN_PWR","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_IN_AMP","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_FAN_RPM","PSU1")
                                                BoardValue=BoardValue.replace("fanpwm_PSU1_FAN_PWM","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_OUT_AMP","PSU1")
                                                BoardValue=BoardValue.replace("PSU1_IN_TMP","PSU1")
                                                BoardValue=BoardValue.replace("fanpwm_PSU2_FAN_PWM","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_IN_VLT","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_OUT_AMP","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_FAN_RPM","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_IN_PWR","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_OUT_VLT","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_OUT_PWR","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_IN_TMP","PSU2")
                                                BoardValue=BoardValue.replace("PSU2_IN_AMP","PSU2")
                                                
                                                xmSensor = str(SENSOR_NAME_LIST[i] + "!"+ClienT  +  "!"+ SerVer2 +"!")
                                                while " " in xmSensor:
                                                    xmSensor=xmSensor.replace(" ","")
                                                end_dict[xmSensor+str(SDRvalue)] = BoardValue#+ "!!!!!!"+RedFishList[i]
                                                
                                                dub = dub + [xmSensor+str(SDRvalue)]
                                                
                                                print(name)
                                                ert = 1
    
    #i=i+1
    print("")#print(len(SENSOR_NAME_LIST))
    print("")#print(len(RedFishList))
    print("")#print(RedFishList)
    print("")#print(all59)
    #ProgressbarState(6)
        
    #print("")#print(DO_LIST)
    #print("")#print("Отмеченные предметы:", items)
        
    #exit()
    #os.remove("ABC.txt") #удаление файлов
    #os.remove("CBA.txt") #удаление файлов
    os.system(sshConnectionString+ipAddr+" touch CBA.txt") #создание пустого файла
    
    x = selected_items



    #Failed to get property Value on interface xyz


    z = end_dict
    
    #{"iphone": "AQUARIUS_AQC621AB_Chassis/", "ipad": "AQUARIUS_AQC621AB_Chassis/", "iead": "AQUARIUS_AQC621AB_Baseboard/"}
    print("")#print(all52)
    print("")#print(all59)
    print("")#print(FixBoardsNames)
    ProgressbarSrceenOFF()
    
    
    
    ExtraGAV = []
    
    ProgressbarState(2)
    ProgressbarState(3)
    ProgressbarState(4)
    ProgressbarState(5)
    ProgressbarState(6)
    ProgressbarState(7)
   

    ForErrorBoardData = 0
    for w in FixBoardsNames:
        z["NoData!NoData!NoData"+str(ForErrorBoardData)] = w
        ForErrorBoardData = ForErrorBoardData + 1
    x = x + ["Server_Chassis"]
    FinalBoardsList = []
    TempCount = 0
    for cat in x:
        print("")#print(cat)
        if TempCount == 0:
            FinalBoardsList = FinalBoardsList + ["Server_Board"]
        if TempCount >= 1:
            FinalBoardsList = FinalBoardsList + [cat]
        TempCount = TempCount + 1
    x = FinalBoardsList
    print("")#print(x)
    print("")#print(z)
    print("")#print(all5)
    print("")#print("-------------------")
    print("")#print(cSDR)
    print("")#print("all52",len(all52))
    print("")#print("all59",len(all59))
    print("")#print("cSDR",len(cSDR))
    print("")#print(all52)
    print("")#print(all59)
    print("")#print("-------------------")
    print("")#print("-------------------")
    print("")#print("-------------------")
    #print("")#print(cONLY_NAME_SENSOR)
    #print("")#print(len(cONLY_NAME_SENSOR))
    print("")#print(all59)
    print("")#print("-------------------")
    print("")#print("-------------------")
    print("")#print("-------------------")
    #print("")#print(sur)
    #print("")#print(end_dict)
    print("")#print(SENSOR_NAME_LIST)
    #print("")#print(RedFishList)
    # Преобразуем строки в список словарей
    
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

    print("")#print("Данные успешно сохранены в paths.json")'''
    #print("")#print(all5SP)
    #print("")#print(end_dict)
    #print("")#print(SENSOR_NAME_LIST)
    #print("")#print(DebugList)
    
    #print("")#print(allSDR)
    #print("")#print("Extra: ",ExtraGAV)#HEATER_TEMP
    #print("")#print("HEATER_TEMP FISH: ",ExtraGAV[0])
    #print("")#print("HEATER_TEMP BUS: ",ExtraGAV[1])
    #print("")#print("HEATER_HUMID FISH: ",ExtraGAV[2])
    #print("")#print("HEATER_HUMID BUS: ",ExtraGAV[3])
    #if len(ExtraGAV) >= 4:
        #z["HEATER_TEMP "+str(ExtraGAV[0])+" "+ str(ExtraGAV[1])+" -"] = "IR-AX-HU1"
        #z["HEATER_HUMID "+str(ExtraGAV[2])+" "+ str(ExtraGAV[3])+" -"] = "IR-AX-HU2"
    #print("")#print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 | grep [0-9] >> Extra.txt")
    #print("")#print(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt")
    #print("")#print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'""'+" >> Extra.txt")
    #print("")#print(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity"+'"'+" >> Extra.txt")
    #print("")#print(all52)
    #print("")#print(allPowerServer[0])
    #print("")#print(z)
    os.system("rm *.txt")
    print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Temperatures"+'"'+" -A7 > Extra.txt && echo ------- >> Extra.txt")
    print(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Temperatures"+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
    print("curl -s -k -u root:0penBmc -X GET "+'"'+"https://"+ipAddr+"/redfish/v1/Chassis/IR_AX_HU_Board/Oem"+'"'+"/Aquarius_Irteya/HeatingUnit | grep "+'"'+"Humidity"+'\\'+'""'+" >> Extra.txt && echo ------- >> Extra.txt")
    print(sshConnectionString+ipAddr+" busctl introspect ru.aq.Irteya.HeatingUnit /xyz/openbmc_project/heaters/_81_16 | grep "+'"'+"Humidity "+'"'+" >> Extra.txt && echo ------- >> Extra.txt")
    #BoardsDataList = []
    if len(information_SP) >= 3:
        BoardsDataList = BoardsDataList +[information_SP[0]]+[information_SP[1]]+[information_SP[2]]
    BoardsDataList=BoardsDataList+["SERVER is "+str(serverstate)+" "+ipAddr]
    updateWINTo2(x, z, BoardsDataList)
    

ipAddr = ""
main_window = None


class ItemSelector(QWidget):
    def __init__(self, items, options_dict, DataBoardsFinalData=None):
        super().__init__()
        self.items = items
        self.options_dict = options_dict
        self.dialogs = {}
        self.DataBoardsFinalData = DataBoardsFinalData or []
        self.setDisabled(False)

        self.layout = QVBoxLayout(self)  # Главный вертикальный layout

        # === Убираем отображение DataBoardsFinalData ===
        self.DataBoardsFinalData_label = QTextEdit(self)
        self.DataBoardsFinalData_label.setReadOnly(True)
        self.DataBoardsFinalData_label.setFixedHeight(100)
        self.DataBoardsFinalData_label.setStyleSheet("background-color: #f0f0f0; font-family: Consolas;")
        if self.DataBoardsFinalData:
            self.DataBoardsFinalData_label.setText("\n".join(self.DataBoardsFinalData))
        else:
            self.DataBoardsFinalData_label.setText("Список пуст или не передан.")
        
        # Убираем DataBoardsFinalData_label с главного окна
        self.DataBoardsFinalData_label.setVisible(False)  # Скрыть виджет

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

            # 🔄 Словарь замен имён "AQRZ2-U4P1-R","AQRZ2_U4P1_R"
            item_replacements = {
                "AQRZ2_U4P1_R": "AQRZ2-U4P1-R",
                "AQFPB_FFC": "AQFPB-FFC",
                # Добавьте нужные замены
            }

            # 🔄 Словарь замен имён (если нужно — можно вынести в init или отдельный метод)
            

            # 🆗 Создаём заменённое имя для анализа, не меняя оригинал
            lookup_item = item_replacements.get(item, item)

            # 🔍 Найдём связанный текст из DataBoardsFinalData, где содержится заменённое имя
            related_lines = [
                line for line in self.DataBoardsFinalData
                if lookup_item in line
            ]

            # Проверим наличие строки "ERROR : NoData" в найденных строках (без учёта регистра)
            is_error_InData = any("ERROR : NoData" in line for line in related_lines)

            # Печатаем строки, которые анализируем
            print("")#print("🔍 Проверяем строки:")
            for line in related_lines:
                print("")#print(f" → {line}")

            # Проверка наличия данных по заменённому имени
            # Проверка наличия данных по заменённому имени и игнор ошибок "NoData" в ключе
            has_data = any(
                item in values and "NoData" not in key
                for key, values in self.options_dict.items()
            )


            # Печатаем результат промежуточных проверок
            print("")#print(f"⚠️ Найдена ошибка (ERROR : NoData): {is_error_InData}")
            print("")#print(f"📊 Есть данные (has_data): {has_data}")

            # Устанавливаем флаги и внешний вид
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)

            if is_error_InData:
                print("")#print("🚫 Элемент отключён из-за ошибки")
                list_item.setFlags(list_item.flags() & ~Qt.ItemIsEnabled)  
                list_item.setForeground(QColor("red"))
                list_item.setCheckState(Qt.Unchecked)
            
            else:
                print("")#print("✅ Элемент доступен для выбора")
                list_item.setCheckState(Qt.Unchecked)

            # Печать добавляемого элемента
            print("")#print(f"➕ Добавлен элемент в список: {list_item.text()}\n")

            # Добавляем в list_widget
            self.list_widget.addItem(list_item)



        left_split.addWidget(self.list_widget)
        #print("")#print(DataBoardsFinalData[len(DataBoardsFinalData)-1])
        print("")#print(DataBoardsFinalData)
                # Таблица с версиями
        

        # IP секция
        ip_section = QWidget()
        ip_layout = QVBoxLayout(ip_section)
        if len(DataBoardsFinalData)>=3:
            font_scale = 0.75
            print("")#print(len(DataBoardsFinalData))
            if "FirmwareVersion" in DataBoardsFinalData[len(DataBoardsFinalData)-2]:
            
                # Обработка строк
                inf0 = str(DataBoardsFinalData[len(DataBoardsFinalData)-4]).replace('",', "")
                
                inf0 = inf0.replace("FirmwareVersion", "BMC Version")
                inf0sp=inf0.split("dev-")
                ainf0 = inf0sp[1]
                binf0=ainf0.split("-")
                cinf0 = binf0[0]
                inf0 = str('"BMC Version": ')+str('"'+cinf0+'"')
                
                
                inf1 = str(DataBoardsFinalData[len(DataBoardsFinalData)-3]).replace('",', "")
                inf1=inf1.replace("BiosVersion","Bios Version")
                
                
                inf2 = str(DataBoardsFinalData[len(DataBoardsFinalData)-2]).replace('",', "")
                inf2=inf2.replace("FirmwareVersion","IR-AX-HU Firmware Version")
                VERsionSP = [inf0, inf1, inf2]

                # Таблица
                self.version_table = QTableWidget()
                self.version_table.setRowCount(len(VERsionSP))
                self.version_table.setColumnCount(2)
                self.version_table.setHorizontalHeaderLabels(["Название", "Версия"])

                # Применение масштабированного шрифта
                base_font = self.version_table.font()
                new_font = QFont(base_font)
                new_font.setPointSizeF(base_font.pointSizeF() * font_scale)
                self.version_table.setFont(new_font)

                # Заполнение таблицы
                for row, item in enumerate(VERsionSP):
                    if '":' in item:
                        try:
                            name, version = item.split('":')
                            name = name.strip().strip('"')
                            version = version.strip().strip('" ')
                            self.version_table.setItem(row, 0, QTableWidgetItem(name))
                            self.version_table.setItem(row, 1, QTableWidgetItem(version))
                        except Exception as e:
                            print("")#print(f"Ошибка при разборе строки: {item}", e)

                # Автоматическая подгонка строк и колонок
                self.version_table.resizeRowsToContents()
                self.version_table.resizeColumnsToContents()

                # Автоматическая подгонка размера таблицы под содержимое
                self.version_table.adjustSize()
                for row in range(self.version_table.rowCount()):
                    self.version_table.setRowHeight(row, self.version_table.sizeHintForRow(row))


                # Добавление в layout
                ip_layout.addWidget(self.version_table)
        ip_layout.setContentsMargins(0, 0, 0, 0)
        
        #self.ip_label = QLabel(" ")
        #self.ip_label.setFixedWidth(900)

        
        # Создание выпадающего списка для ввода IP-адреса
        #self.ip_combo = QComboBox(self)
        #self.ip_combo.setPlaceholderText("Например: 192.168.0.10")
        
        # Загрузка IP-адресов из JSON
        #self.load_ip_addresses_from_json()

        #self.ip_input = QLineEdit(self)
        #self.ip_input.setPlaceholderText("Введите новый IP, если его нет в списке.")
        
        #self.confirm_button = QPushButton("Подтвердить")
        #self.confirm_button.clicked.connect(self.confirm_ip)

        # Кнопки ВКЛ и ВЫКЛ
        self.buttons_layout = QHBoxLayout()  # Горизонтальный layout для кнопок
        
        # Обработка статуса и IP
        def turn_on(self):
            global ipAddr
            print("")#print(f"Включение устройства с IP: {ipAddr}")
            # Замените на вашу команду для включения
            os.system(sshConnectionString+ipAddr+" ipmitool power on")

        def turn_off(self):
            global ipAddr
            print("")#print(f"Выключение устройства с IP: {ipAddr}")
            # Замените на вашу команду для выключения
            os.system(sshConnectionString+ipAddr+" ipmitool power off")
        # Предположим, это у тебя внутри класса (например, в `__init__` или методе)
        last_status_full = DataBoardsFinalData[len(DataBoardsFinalData)-1]
        parts = last_status_full.strip().split()
        ip = parts[-1]
        status = ' '.join(parts[:-1])
        print("")#print("IP-адрес:", ip)

        self.server_ip = ip
        self.current_status = 'on' if status == 'SERVER is on' else 'off'
        self.ip2_label = QLabel(ip)
        self.ip2_label.setFixedWidth(700)
        self.i1p_label = QLabel()
        self.i1p_label.setCursor(QCursor(Qt.PointingHandCursor))

        def update_label():
            if self.current_status == 'on':
                icon_path = "ServerIsOn.png"
                status_text = "Server is on"
            else:
                icon_path = "ServerIsOff.png"
                status_text = "Server is off"

            # HTML с увеличенной иконкой (60x60)
            html = f'''
                <span>
                    <img src="{icon_path}" width="40" height="40" style="vertical-align: middle;">
                    <span style="font-size:40px; color:{'green' if self.current_status == 'on' else 'gray'};"> {status_text}</span>
                </span>
            '''
            self.i1p_label.setText(html)

        update_label()


        def handle_label_click(event):
            if self.current_status == 'on':
                turn_off(self.server_ip)
                self.current_status = 'off'
            else:
                turn_on(self.server_ip)
                self.current_status = 'on'
            update_label()

        self.i1p_label.mousePressEvent = handle_label_click


        
        

        


        # Подключение сигнала выбора IP из комбобокса к полю ввода
        #self.ip_combo.currentTextChanged.connect(self.update_ip_input_from_combo)

        #ip_layout.addWidget(self.ip_label)
        
        #ip_layout.addWidget(self.ip_combo)  # Добавляем комбобокс вместо поля ввода
        #ip_layout.addWidget(self.ip_input)  # Оставляем поле ввода для новых IP
        #ip_layout.addWidget(self.confirm_button)

        # Добавляем кнопки
        ip_layout.addLayout(self.buttons_layout)
        #ip2_label
        ip_layout.addWidget(self.ip2_label)

        ip_layout.addWidget(self.i1p_label)

        # Размещение в левом разделе (если он есть)
        left_split.addWidget(ip_section)


        #print("")#print(DataBoardsFinalData[-4])
        #print("")#print(DataBoardsFinalData[-3])
        #print("")#print(DataBoardsFinalData[-2])


        # Таблица
        self.main_table = QTableWidget(self)
        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels(["Sensor", "RedFish", "D-Bus", "Ipmitool"])
        font = QFont("Courier New", 10)
        font.setPointSizeF(font.pointSizeF() * 0.8)
        self.main_table.setFont(font)
        
        main_h_layout.addWidget(self.main_table, 4)

        self.list_widget.itemChanged.connect(self.on_item_changed)

    

    def update_ip_input_from_combo(self, text):
        # Автозаполнение поля ввода при выборе IP из списка
        self.ip_input.setText(text)

    
    
    def turn_on(self):
        global ipAddr
        print("")#print(f"Включение устройства с IP: {ipAddr}")
        # Замените на вашу команду для включения
        os.system(sshConnectionString+ipAddr+" ipmitool power on")

    def turn_off(self):
        global ipAddr
        print("")#print(f"Выключение устройства с IP: {ipAddr}")
        # Замените на вашу команду для выключения
        os.system(sshConnectionString+ipAddr+" ipmitool power off")


        


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
        bad_values = {"nan", "null", "0.0", "0.00", "0V", "0W", "0A", "0°C", "0%", "0RPM", "noreading", "NotInstalled", "disabled"}
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
                header_text = self.DataBoardsFinalData[idx] if idx < len(self.DataBoardsFinalData) else ""
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

        bad_values = {"nan", "null", "0.0", "0.00", "0V", "0W", "0A", "0°C", "0%", "0RPM", "noreading", "NotInstalled", "disabled"}
        elements = text.split('\n')

        valid_elements = []
        line_detected = False
        candidate = None

        for element in elements:
            parts = element.strip().split("!")
            if len(parts) == 3 and parts[0] == "NoData" and parts[1] == "NoData" and parts[2].startswith("NoData") and parts[2][6:].isdigit():
                line_detected = True
                candidate = element.strip()
                continue
            if element.strip():
                valid_elements.append(element.strip())

        if line_detected and len(valid_elements) == 0:
            valid_elements.append("__NO_SENSOR_ERROR__")

        row_index = 0
        for element in valid_elements:
            if element == "__NO_SENSOR_ERROR__":
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
        self.setGeometry(0, 0, 2100, 1350)
        self.setFixedSize(2100, 1350)

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

        with open('ipadr.json', 'r') as file:
            ip_data = json.load(file)

        dialog = QDialog(self)
        dialog.setWindowTitle("Введите IP-адрес")
        dialog.setMinimumSize(500, 250)

        layout = QVBoxLayout(dialog)

        ip_input = QLineEdit(dialog)
        layout.addWidget(ip_input)

        ip_combo = QComboBox(dialog)
        ip_combo.addItem("Выбрать IP")
        for entry in ip_data:
            ip_combo.addItem(entry["IP"])
        layout.addWidget(ip_combo)

        ok_button = QPushButton("OK", dialog)
        ok_button.setEnabled(False)
        layout.addWidget(ok_button)

        def on_ip_changed():
            ip = ip_input.text().strip()
            ok_button.setEnabled(False)
            if self.is_valid_ip_format(ip):
                self.ping_ip(ip, lambda success: ok_button.setEnabled(success))

        # При выборе IP из выпадающего списка — подставить в поле ввода
        ip_combo.currentIndexChanged.connect(
            lambda: ip_input.setText(ip_combo.currentText() if ip_combo.currentIndex() > 0 else "")
        )

        # Обработка ввода вручную
        ip_input.textChanged.connect(on_ip_changed)

        ok_button.clicked.connect(lambda: self.on_ok_pressed(ip_input.text(), ip_combo.currentText(), dialog))

        dialog.exec_()

    def is_valid_ip_format(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            n = int(part)
            if n < 0 or n > 255:
                return False
        return True

    def ping_ip(self, ip, callback):
        def run_ping():
            try:
                # Windows: -n, Unix-like: -c
                cmd = ["ping", "-n" if sys.platform == "win32" else "-c", "1", ip]
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                success = result.returncode == 0
            except Exception:
                success = False
            QTimer.singleShot(0, lambda: callback(success))

        QTimer.singleShot(100, run_ping)

    def on_ok_pressed(self, ip_input_value, ip_combo_value, dialog):
        global ipAddr
        dialog.accept()

        if ip_input_value.strip():
            ipAddr = ip_input_value
        elif ip_combo_value.strip() and ip_combo_value != "Выбрать IP":
            ipAddr = ip_combo_value
        else:
            ipAddr = "172.26.24.14"

        self.label.setText(f"Используется IP: {ipAddr}")
        StartProgramm(ipAddr)

    

    def turn_on(self, ip_input_value):
        global ipAddr
        ipAddr = ip_input_value.strip() if ip_input_value.strip() else "172.26.24.14"
        print("")#print("Выключение устройства")
        os.system(sshConnectionString+ipAddr+" ipmitool power on")

    def turn_off(self, ip_input_value):
        global ipAddr
        ipAddr = ip_input_value.strip() if ip_input_value.strip() else "172.26.24.14"
        print("")#print("Выключение устройства")
        os.system(sshConnectionString+ipAddr+" ipmitool power off")

    def updateWINTo2(self, x, y, DataBoardsFinalData=None):
        if self.page2:
            self.stack.removeWidget(self.page2)
            self.page2.deleteLater()

        self.page2 = ItemSelector(x, y, DataBoardsFinalData)
        self.stack.addWidget(self.page2)
        self.stack.setCurrentWidget(self.page2)

    def closeEvent(self, event):
        print("")#print("Закрытие приложения и всех окон.")
        QApplication.quit()



def updateWINTo2(x, z, DataBoardsFinalData=None):
    if main_window:
        main_window.updateWINTo2(x, z, DataBoardsFinalData)
# === Глобальные переменные ===
overlay_widget = None
progress_overlay = None
progress_dots = []
progress_labels = []
progress_bar = None
main_window = None  # <- должен быть определён в __main__


def ProgressbarSrceenON():
    """
    Показывает затемнение с 7 точками, подписями и прогресс-баром.
    Подписи берутся из массива внутри этой функции.
    """
    global overlay_widget, progress_overlay, progress_dots, progress_labels, progress_bar, main_window

    if not main_window:
        print("")#print("❌ main_window is not set.")
        return

    # Сбросим всё, если уже было
    ProgressbarSrceenOFF()

    # === Встроенный массив подписей ===
    progress_texts = ["Очистка Системы", "Получение названий плат", "Получение деревьев BUCSTL", "Получение информации по BUCSTL", "Получение информации по RedFish", "Создание общего списка", "Передача данных в интерфейс"]

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



def ProgressbarState(j):
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


def ProgressbarSrceenOFF():
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
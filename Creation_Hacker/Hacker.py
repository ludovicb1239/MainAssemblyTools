"""
@author: Ludovic
"""

import os
import time
import sys

currentDir = os.getcwd()
Name = input("Creation's name : ")
try:
    ImportedBot = open(os.path.expandvars(r'%LOCALAPPDATA%\RoboBuild\Saved\bots\.bot.' + Name + '/' + Name + '.schematic.json'),"r")
except:
    print(Name + ".schematic.json not found, please read the instructions")
    pause = input("Press Enter to continue ")
    sys.exit(1)
partToHack = input("Hacking part (jet_engine) ")
juice = input("New hacked juice value (%) ")
number = input(partToHack + " number (01 or more) ")
FinalCode = ImportedBot.readlines()
line = 0
ImportedBot.close()
i = 0
for code in FinalCode:
    FinalCode[i] = code[:-1]
    i+=1
print("\nSucessfully imported bot")
StartedTime = time.process_time()
timeStart = time.process_time()
while (line < len(FinalCode) - 1):
    if (FinalCode[line].startswith( '\t\t"' + partToHack + '_' + number)):
        FinalCode[line + 19] = '\t\t\t\t\t"Juice": { "tag": "EProperty_Float", "float": ' + juice +' },'
    if (timeStart + 0.5 < time.process_time()):
        percent = int(line / len(FinalCode) * 100)
        left = 30 * percent // 100
        right = 30 - left
        print('\r[', '#' * left, ' ' * right, ']', f' {percent:.0f}%', sep='', end='', flush=True)
        timeStart = time.process_time()
    line+=1
percent = 100
left = 30 * percent // 100
right = 30 - left
print('\r[', '#' * left, ' ' * right, ']', f' {percent:.0f}%', sep='', end='', flush=True)
print("\n\nSucessfully Converted " + Name + ".schematic.json bot in " + str(int((time.process_time() - StartedTime) * 10) / 10) + " seconds")
OutputJSON = open(os.path.expandvars(r'%LOCALAPPDATA%\RoboBuild\Saved\bots\.bot.' + Name + '/' + Name + '.schematic.json'),"w")
for printingLine in FinalCode:
    OutputJSON.write(printingLine + "\n")
OutputJSON.write("}")
OutputJSON.close()
print("\nSucessfully replaced bot")
pause = input("\nPress Enter to continue ")
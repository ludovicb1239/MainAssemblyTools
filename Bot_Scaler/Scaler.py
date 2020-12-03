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
print("\nZ\nXY\n\nX : Forward\nY : Right\nZ : Up")
ScaleX = float(input("Creation's X scale : "))
ScaleY = float(input("Creation's Y scale : "))
ScaleZ = float(input("Creation's Z scale : "))
FinalCode = ImportedBot.readlines()
line = 0
writing = False
ImportedBot.close()
i = 0
for code in FinalCode:
    FinalCode[i] = code[:-1]
    i+=1
print("\nSucessfully imported bot")
PrintedError1 = False
print("\nStarting scaling bot\n")
StartedTime = time.process_time()
timeStart = time.process_time()
while (line < len(FinalCode) - 1):
    if (writing):
        Pos = (FinalCode[line]).split()
        pointNum = Pos[0]
        xPos = str(float((Pos[3])[:-1]) * ScaleX)
        yPos = str(float((Pos[5])[:-1]) * ScaleY)
        zPos = str(float((Pos[7])) * ScaleZ)
        FinalCode[line] = '\t\t\t\t' + pointNum + ' { "x": ' + xPos + ', "y": ' + yPos + ', "z": ' + zPos + " " + Pos[8]
    if (str(FinalCode[line]) == '\t\t\t"points": {'):
        writing = True
    if (FinalCode[line + 1] == '\t\t\t},' and writing):
        writing = False
    if (FinalCode[line].startswith( '\t\t\t\t\t"curveControl": {' )):
        Pos = (FinalCode[line]).split()
        xPos = str(float((Pos[3])[:-1]) * ScaleX)
        yPos = str(float((Pos[5])[:-1]) * ScaleY)
        zPos = str(float((Pos[7])) * ScaleZ)
        FinalCode[line] = '\t\t\t\t\t"curveControl": { "x": ' + xPos + ', "y": ' + yPos + ', "z": ' + zPos + " " + Pos[8]
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
print("\nSucessfully remplace bot")
pause = input("\nPress Enter to continue ")
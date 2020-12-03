"""
@author: Ludovic
"""

import os
import shutil
import time
import sys

currentDir = os.getcwd()
Name = input("Creation's name : ")
try:
    ImportedOBJ = open((currentDir+"\\" + Name + ".obj"),"r")
except:
    print(Name + ".obj not found or not readable, please read the instructions")
    pause = input("Press Enter to continue ")
    sys.exit(1)
print("\nZ\nXY\n\nX : Forward\nY : Right\nZ : Up")
ScaleX = float(input("Creation's X scale : "))
ScaleY = float(input("Creation's Y scale : "))
ScaleZ = float(input("Creation's Z scale : "))
CreationForward = input("Your creation's forward (X or Y or Z) ")
InvertZY = int(input("Invert Z axis over Y (1 or 0) "))
RoundVertexPos = int(input("Round Vertex Position to 1.25cm (Grid) (1 or 0) "))
Mirror = int(input("Mirror Creation on Y Axis (1 or 0) "))
ShowFrameSegments = input("Show frame segments (true or false) ")
try:
    BaseJSON = open((currentDir+"\BaseCode.json"),"r")
except:
    print(Name + "BaseCode.json not found or not readable, please read the instructions")
    pause = input("Press Enter to continue ")
    sys.exit(1)
ImportedInfo = ImportedOBJ.readlines()
line = 0
FinalCode = BaseJSON.readlines()
BaseJSON.close()
ImportedOBJ.close()
i = 0
for code in FinalCode:
    FinalCode[i] = code[:-1]
    i+=1
print("\nSucessfully imported 3d model")
FinalCode[46] = '\t\t\t"mirror": "MirrorY",'
pointNum = 1
faceNum = 1
PrintedError1 = False
PrintedError2 = False
Parts = 0
if (len(ImportedInfo) > 100000):
    print("\n\nYour model is heavy, you might want to use another one\n")
print("\nStarting converting model\n")
StartedTime = time.process_time()
timeStart = time.process_time()
NotMirroredPoints = []
segments = [] #(first, second)    x, y, z
while (line < len(ImportedInfo)):
    if (ImportedInfo[line].startswith("v ")):
        Pos = ((ImportedInfo[line])[2:-1]).split()
        if (CreationForward == "X"):
            xPos = Pos[0] 
            yPos = Pos[1 + InvertZY]
            zPos = Pos[2 - InvertZY]
        elif (CreationForward == "Y"):
            xPos = Pos[1]
            yPos = Pos[0 + (InvertZY * 2)]
            zPos = Pos[2 - (InvertZY * 2)]
        elif (CreationForward == "Z"):
            xPos = Pos[2]
            yPos = Pos[1 - InvertZY]
            zPos = Pos[0 + InvertZY]
        if (Mirror and float(yPos) < 0):
            NotMirroredPoints.append(int(pointNum))
            yPos = "0"
        if (RoundVertexPos == 1):
            xPos = str(int(float(xPos) * ScaleX * 0.8) / 0.8)
            if (not yPos == "0"):
                yPos = str(int(float(yPos) * ScaleY * 0.8) / 0.8)
            zPos = str(int(float(zPos) * ScaleZ * 0.8) / 0.8)
        else:
            xPos = str(float(xPos) * ScaleX)
            if (not yPos == "0"):
                yPos = str(float(yPos) * ScaleY)
            zPos = str(float(zPos) * ScaleZ)
        vertexCount = 0
        for i in ImportedInfo:
            if (i.startswith("v ")):
                vertexCount += 1
        period = vertexCount > pointNum
        writingLine = 0
        for lookingLine in FinalCode:
            if (lookingLine == '\t\t\t"frameSegments": {'):
                break;
            writingLine += 1
        FinalCode.insert(writingLine - 1, "\t\t\t\t" + '"' + str(pointNum) + '"' + """: { "x": """ + xPos + """, "y": """ + yPos + """, "z": """ + zPos + " }" + ("," * period))
        pointNum += 1
    elif (ImportedInfo[line].startswith("f")):
        Points = ((ImportedInfo[line])[2:-1]).split()
        i = 0
        for vertexPoint in Points:
	        coordinates = vertexPoint.split("/")
	        Points[i] = coordinates[0]
	        i += 1
        AllOnMirrorSize = "true"
        for mirrorPoint in Points:
            if (not int(mirrorPoint) in NotMirroredPoints):
                AllOnMirrorSize = "false"
        if (AllOnMirrorSize == "false"):
            facesCount = 0
            for i in ImportedInfo:
                if (i.startswith("f")):
                    facesCount += 1
            period = facesCount > faceNum
            writingLine = 0
            for lookingLine in FinalCode:
                if (lookingLine == '\t\t\t"locked": false,'):
                    break;
                writingLine += 1
            FinalCode.insert(writingLine - 2, "\t\t\t\t}" + ("," * period))
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t\t" + '} }')        
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t\t\t" + '"material": { "tag": "EProperty_Int", "integer": 0 }')
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t\t\t" + '"tint": { "tag": "EProperty_Tint", "integer": 0 },')
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t\t" + '"values": {')
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t" + '"properties": {')
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t" + '"visible": true,')
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t" + '],')
            i = len(Points) - 1
            while (i > -1):
                if (len(Points) - 1 == i):
                    FinalCode.insert(writingLine - 2, '\t\t\t\t\t\t{ "elemId": ' + Points[i] + " }")
                else:
                    FinalCode.insert(writingLine - 2, '\t\t\t\t\t\t{ "elemId": ' + Points[i] + " },")
                i -= 1
            FinalCode.insert(writingLine - 2, "\t\t\t\t\t" + '"points": [')
            FinalCode.insert(writingLine - 2, "\t\t\t\t" + '"' + str(faceNum) + '"' + ": {")
        faceNum += 1
        i = 0
        while (i < len(Points) - 1):
            segmentInfo = (Points[i], Points[i + 1])
            invertedSegmentInfo = (Points[i + 1], Points[i])
            if (not segmentInfo in segments and not invertedSegmentInfo in segments):
                segments.append(segmentInfo)
            i += 1
        segmentInfo = (Points[0], Points[i])
        invertedSegmentInfo = (Points[i], Points[0])
        if (not segmentInfo in segments and not invertedSegmentInfo in segments):
            segments.append(segmentInfo)
    elif ImportedInfo[line].startswith("vp") and not PrintedError1:
        print("\nYour model contains Free-form geometry statements, you might want to use another one")
        PrintedError1 = True
    elif ImportedInfo[line].startswith("o "):
        Parts += 1
    if ImportedInfo[line].startswith("o ") and not PrintedError2 and Parts == 2:
        print("\nYour model contains multiple parts, you might want to use another one")
        PrintedError2 = True
    if (timeStart + 0.5 < time.process_time()):
        percent = int(line / len(ImportedInfo) * 100)
        left = 30 * percent // 100
        right = 30 - left
        print('\r[', '#' * left, ' ' * right, ']', f' {percent:.0f}%', sep='', end='', flush=True)
        timeStart = time.process_time()
    line+=1
print("\nFinishing converting 3d model..")
segmentNum = 1
segmentCount = len(segments)
while (segmentNum < segmentCount):
    second, first = segments[segmentNum - 1]
    if (not ((int(second) in NotMirroredPoints) and (int(first) in NotMirroredPoints))):
        period = segmentCount - 1 > segmentNum
        writingLine = 0
        for lookingLine in FinalCode:
            if (lookingLine == '\t\t\t"framePlates": {'):
                break;
            writingLine += 1
        FinalCode.insert(writingLine - 1, "\t\t\t\t}" + ("," * period))
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t\t" + '} }')        
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t\t\t" + '"material": { "tag": "EProperty_Int", "integer": 1 }')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t\t\t" + '"tint": { "tag": "EProperty_Tint", "integer": 2 },')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t\t" + '"values": {')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t" + '"properties": {')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t" + '"visible": ' + ShowFrameSegments + ",")
        #FinalCode.insert(writingLine - 1, "\t\t\t\t\t" + '"curveControl": { "x": 0, "y": 0, "z": 0 },"')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t" + '"second": { "elemId": ' + second + ' },')
        FinalCode.insert(writingLine - 1, "\t\t\t\t\t" + '"first": { "elemId": ' + first + ' },')
        FinalCode.insert(writingLine - 1, "\t\t\t\t" + '"' + str(segmentNum) + '": {')
    segmentNum += 1
percent = 100
left = 30 * percent // 100
right = 30 - left
print('\r[', '#' * left, ' ' * right, ']', f' {percent:.0f}%', sep='', end='', flush=True)
print("\n\nSucessfully Converted " + Name + ".obj model in " + str(int((time.process_time() - StartedTime) * 10) / 10) + " seconds")
try:
    OutputJSON = open((currentDir+"\Output\Output.schematic.json"),"w")
except:
    print(Name + "\Output\Output.schematic.json not found or not writable, please read the instructions")
    pause = input("Press Enter to continue ")
    sys.exit(1)
for printingLine in FinalCode:
    OutputJSON.write(printingLine + "\n")
OutputJSON.close()
print("\nSucessfully Saved Converted model")
try:
    shutil.rmtree(os.path.expandvars(r'%LOCALAPPDATA%\RoboBuild\Saved\bots\.bot.Output/'))
except:
    print("\nFirst time converting " + Name + ", creating new bot...")
time.sleep(0.5)
shutil.copytree ((currentDir+"\Output\\"), os.path.expandvars(r'%LOCALAPPDATA%\RoboBuild\Saved\bots\.bot.Output/'))
time.sleep(0.5)
print("\nSucessfully Created a new bot")
pause = input("\nPress Enter to continue ")
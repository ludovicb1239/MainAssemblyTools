"""
@author: ludovicb1239
"""
#For free form curve use
#curv point x y z
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
CreationForward.capitalize()
InvertZY = int(input("Invert Z axis over Y (1 or 0) "))
RoundVertexPos = int(input("Round Vertex Position to 1.25cm (Grid) (1 or 0) "))
Mirror = int(input("Mirror Creation on Y Axis (1 or 0) "))
ShowFrameSegments = input("Show frame segments (true or false) ")
ShowFrameSegments.lower()
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
vertexCount = 0
for i in ImportedInfo:
    if (i.startswith("v ")):
        vertexCount += 1
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
NotMirroredCurvs = []#(first, second)
segments = [] #(first, second)    x, y, z
curves = [] #firstPoint secondPoint x y z
vertexes = [] #(x, y, z)
while (line < len(ImportedInfo)):
    if (ImportedInfo[line].startswith("v ")):
        Pos = ((ImportedInfo[line])[2:-1]).split()            
        xPos = 0
        yPos = 0
        zPos = 0
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
        period = vertexCount > pointNum
        writingLine = 0
        for lookingLine in FinalCode:
            if (lookingLine == '\t\t\t"frameSegments": {'):
                break;
            writingLine += 1
        FinalCode.insert(writingLine - 1, "\t\t\t\t" + '"' + str(pointNum) + '"' + """: { "x": """ + xPos + """, "y": """ + yPos + """, "z": """ + zPos + " }" + ("," * period))
        pointNum += 1
        vertexes.append((xPos, yPos, zPos))
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
            nowWritingLine = writingLine - 2
            FinalCode.insert(nowWritingLine, "\t\t\t\t}" + ("," * period))
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t" + '} }')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t\t" + '"material": { "tag": "EProperty_Int", "integer": 0 }')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t\t" + '"tint": { "tag": "EProperty_Tint", "integer": 0 },')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t" + '"values": {')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"properties": {')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"visible": true,')
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '],')
            i = len(Points) - 1
            while (i > -1):
                if (len(Points) - 1 == i):
                    FinalCode.insert(nowWritingLine, '\t\t\t\t\t\t{ "elemId": ' + Points[i] + " }")
                else:
                    FinalCode.insert(nowWritingLine, '\t\t\t\t\t\t{ "elemId": ' + Points[i] + " },")
                i -= 1
            FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"points": [')
            FinalCode.insert(nowWritingLine, "\t\t\t\t" + '"' + str(faceNum) + '"' + ": {")
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
    elif (ImportedInfo[line].startswith("curv ")): #first second x1 y1 z1 x2 y2 z2
        curveInfo = ((ImportedInfo[line])[5:-1]).split()
        firstPoint = curveInfo[0]
        secondPoint = curveInfo[1]
        firstControl = [0,0,0]
        secondControl = [0,0,0]
        if (CreationForward == "X"):
            firstControl[0] = curveInfo[2]
            firstControl[1] = curveInfo[3 + InvertZY]
            firstControl[2] = curveInfo[4 - InvertZY]
            secondControl[0] = curveInfo[5]
            secondControl[1] = curveInfo[6 + InvertZY]
            secondControl[2] = curveInfo[7 - InvertZY]
        elif (CreationForward == "Y"):
            firstControl[0] = curveInfo[3]
            firstControl[1] = curveInfo[2 + (InvertZY * 2)]
            firstControl[2] = curveInfo[4 - (InvertZY * 2)]
            secondControl[0] = curveInfo[6]
            secondControl[1] = curveInfo[5 + (InvertZY * 2)]
            secondControl[2] = curveInfo[7 - (InvertZY * 2)]
        elif (CreationForward == "Z"):
            firstControl[0] = curveInfo[4]
            firstControl[1] = curveInfo[3 - InvertZY]
            firstControl[2] = curveInfo[2 + InvertZY]
            secondControl[0] = curveInfo[7]
            secondControl[1] = curveInfo[6 - InvertZY]
            secondControl[2] = curveInfo[5 + InvertZY]
        if (Mirror and float(firstControl[1]) < 0):
            NotMirroredCurvs.append((firstPoint, secondPoint))
            firstControl[1] = "0"
        if (Mirror and float(secondControl[1]) < 0):
            NotMirroredCurvs.append((firstPoint, secondPoint))
            secondControl[1] = "0"
        if (RoundVertexPos == 1):
            firstControl[0] = str(int(float(firstControl[0]) * ScaleX * 0.8) / 0.8)
            if (not firstControl[1] == "0"):
                firstControl[1] = str(int(float(firstControl[1]) * ScaleY * 0.8) / 0.8)
            firstControl[2] = str(int(float(firstControl[2]) * ScaleZ * 0.8) / 0.8)
            secondControl[0] = str(int(float(secondControl[0]) * ScaleX * 0.8) / 0.8)
            if (not secondControl[1] == "0"):
                secondControl[1] = str(int(float(secondControl[1]) * ScaleY * 0.8) / 0.8)
            secondControl[2] = str(int(float(secondControl[2]) * ScaleZ * 0.8) / 0.8)
        else:
            firstControl[0] = str(float(firstControl[0]) * ScaleX)
            if (not firstControl[1] == "0"):
                firstControl[1] = str(float(firstControl[1]) * ScaleY)
            firstControl[2] = str(float(firstControl[2]) * ScaleZ)
            secondControl[0] = str(float(secondControl[0]) * ScaleX)
            if (not secondControl[1] == "0"):
                secondControl[1] = str(float(secondControl[1]) * ScaleY)
            secondControl[2] = str(float(secondControl[2]) * ScaleZ)
        curves.append([firstPoint, secondPoint, firstControl[0], firstControl[1], firstControl[2], secondControl[0], secondControl[1], secondControl[2]])
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
        nowWritingLine = writingLine - 1
        FinalCode.insert(nowWritingLine, "\t\t\t\t}" + ("," * period))
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t" + '} }')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t\t" + '"material": { "tag": "EProperty_Int", "integer": 1 }')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t\t" + '"tint": { "tag": "EProperty_Tint", "integer": 2 },')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t\t" + '"values": {')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"properties": {')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"visible": ' + ShowFrameSegments + ",")
        for curve in curves:
            if curve[0] == first and curve[1] == second:
                z0 = vertexes[int(first)-1]
                z1 = vertexes[int(second)-1]
                c0 = (curve[2], curve[3], curve[4])
                c1 = (curve[5], curve[6], curve[7])
                m0 = ((float(z0[0])+float(c0[0]))/2, (float(z0[1])+float(c0[1]))/2, (float(z0[2])+float(c0[2]))/2)
                m2 = ((float(z1[0])+float(c1[0]))/2, (float(z1[1])+float(c1[1]))/2, (float(z1[2])+float(c1[2]))/2)
                m1 = ((float(c0[0])+float(c1[0]))/2, (float(c0[1])+float(c1[1]))/2, (float(c0[2])+float(c1[2]))/2)
                m3 = ((float(m0[0])+float(m1[0]))/2, (float(m0[1])+float(m1[1]))/2, (float(m0[2])+float(m1[2]))/2)
                m4 = ((float(m2[0])+float(m1[0]))/2, (float(m2[1])+float(m1[1]))/2, (float(m2[2])+float(m1[2]))/2)
                m5 = ((float(m3[0])+float(m4[0]))/2, (float(m3[1])+float(m4[1]))/2, (float(m3[2])+float(m4[2]))/2)
                curveControl = (str(m5[0]), str(m5[1]), str(m5[2]))
                FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"curveControl": { "x": ' + curveControl[0] + ', "y": ' + curveControl[1] + ', "z": ' + curveControl[2] + ' },"')
            if curve[1] == first and curve[0] == second:
                z0 = vertexes[int(first)-1]
                z1 = vertexes[int(second)-1]
                c1 = (curve[2], curve[3], curve[4])
                c0 = (curve[5], curve[6], curve[7])
                m0 = ((float(z0[0])+float(c0[0]))/2, (float(z0[1])+float(c0[1]))/2, (float(z0[2])+float(c0[2]))/2)
                m2 = ((float(z1[0])+float(c1[0]))/2, (float(z1[1])+float(c1[1]))/2, (float(z1[2])+float(c1[2]))/2)
                m1 = ((float(c0[0])+float(c1[0]))/2, (float(c0[1])+float(c1[1]))/2, (float(c0[2])+float(c1[2]))/2)
                m3 = ((float(m0[0])+float(m1[0]))/2, (float(m0[1])+float(m1[1]))/2, (float(m0[2])+float(m1[2]))/2)
                m4 = ((float(m2[0])+float(m1[0]))/2, (float(m2[1])+float(m1[1]))/2, (float(m2[2])+float(m1[2]))/2)
                m5 = ((float(m3[0])+float(m4[0]))/2, (float(m3[1])+float(m4[1]))/2, (float(m3[2])+float(m4[2]))/2)
                curveControl = (str(m5[0]), str(m5[1]), str(m5[2]))
                FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"curveControl": { "x": ' + curveControl[0] + ', "y": ' + curveControl[1] + ', "z": ' + curveControl[2] + ' },"')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"second": { "elemId": ' + second + ' },')
        FinalCode.insert(nowWritingLine, "\t\t\t\t\t" + '"first": { "elemId": ' + first + ' },')
        FinalCode.insert(nowWritingLine, "\t\t\t\t" + '"' + str(segmentNum) + '": {')
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

from afflex import AffFile

filePath = input("file path: ")
forward = float(input("forward time stamp: "))


affString = ""

with open(filePath, "r") as f:
    affString = f.read()

affFile = AffFile()
affFile.load(affString)
affFile.TimingPointDensityFactor = str(int(affFile.TimingPointDensityFactor))
affFile.AudioOffset = str(int(affFile.AudioOffset))

for i in range(len(affFile.Elements)):
    if affFile.Elements[i].name == "timing":
        t, bpm = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
        if t != 0:
            t -= forward
            bpm *= 1
            t = int(t)
            bpm = float(int(100 * bpm)/100)
            affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t), str(bpm)
    elif affFile.Elements[i].name == "hold":
        t1, t2 = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
        t1 -= forward
        t2 -= forward
        t1, t2 = int(t1), int(t2)
        affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t1), str(t2)
    elif affFile.Elements[i].name == "":
        t = float(affFile.Elements[i].arglist[0])
        t -= forward
        t = int(t)
        affFile.Elements[i].arglist[0] = str(t)
    elif affFile.Elements[i].name == "arc":
        t1, t2 = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
        t1 -= forward
        t2 -= forward
        t1, t2 = int(t1), int(t2)
        affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t1), str(t2)
        if len(affFile.Elements[i].follist) != 0:
            for j in range(len(affFile.Elements[i].follist)):
                t = float(affFile.Elements[i].follist[j].arglist[0])
                t -= forward
                t = int(t)
                affFile.Elements[i].follist[j].arglist[0] = str(t)
    elif affFile.Elements[i].name == "scenecontrol":
        if True:#affFile.Elements[i].arglist[1] == "enwidencamera" or affFile.Elements[i].arglist[1] == "enwidenlanes":
            tstart = int(affFile.Elements[i].arglist[0])
            tstart -= forward
            affFile.Elements[i].arglist[0] = str(tstart)


for k in range(len(affFile.TimingGroups)):
    print("timinggroup")
    for i in range(len(affFile.TimingGroups[k].Elements)):
        if affFile.TimingGroups[k].Elements[i].name == "timing":
            t, bpm = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
            if t != 0:
                t -= forward
                bpm *= 1
                t = int(t)
                bpm = float(int(100 * bpm)/100)
                affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t), str(bpm)
        elif affFile.TimingGroups[k].Elements[i].name == "hold":
            t1, t2 = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
            t1 -= forward
            t2 -= forward
            t1, t2 = int(t1), int(t2)
            affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t1), str(t2)
        elif affFile.TimingGroups[k].Elements[i].name == "":
            t = float(affFile.TimingGroups[k].Elements[i].arglist[0])
            t -= forward
            t = int(t)
            affFile.TimingGroups[k].Elements[i].arglist[0] = str(t)
        elif affFile.TimingGroups[k].Elements[i].name == "arc":
            t1, t2 = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
            t1 -= forward
            t2 -= forward
            t1, t2 = int(t1), int(t2)
            affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t1), str(t2)
            if len(affFile.TimingGroups[k].Elements[i].follist) != 0:
                for j in range(len(affFile.TimingGroups[k].Elements[i].follist)):
                    t = float(affFile.TimingGroups[k].Elements[i].follist[j].arglist[0])
                    t -= forward
                    t = int(t)
                    affFile.TimingGroups[k].Elements[i].follist[j].arglist[0] = str(t)
        elif affFile.TimingGroups[k].Elements[i].name == "scenecontrol":
            print(affFile.TimingGroups[k].Elements[i].arglist[1])
            if True:#affFile.TimingGroups[k].Elements[i].arglist[1] == "enwidencamera" or affFile.TimingGroups[k].Elements[i].arglist[1] == "enwidenlanes":
                tstart= int(affFile.TimingGroups[k].Elements[i].arglist[0])
                tstart -= forward
                affFile.TimingGroups[k].Elements[i].arglist[0] = str(tstart)



with open("produced.aff", "w+") as f:
    f.write(affFile.toString())
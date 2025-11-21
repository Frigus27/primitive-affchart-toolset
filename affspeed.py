from afflex import AffFile

def make_speed(affFile: AffFile, speed: float) -> AffFile:
    '''Make the affFile speeded.'''
    coe = 1 / speed
    affFile.AudioOffset = str(int(int(affFile.AudioOffset) * coe))
    for i in range(len(affFile.Elements)):
        if affFile.Elements[i].name == "timing":
            t, bpm = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
            t *= coe
            bpm *= speed
            t = int(t)
            bpm = float(int(100 * bpm)/100)
            affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t), str(bpm)
        elif affFile.Elements[i].name == "hold":
            t1, t2 = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
            t1 *= coe
            t2 *= coe
            t1, t2 = int(t1), int(t2)
            affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t1), str(t2)
        elif affFile.Elements[i].name == "":
            t = float(affFile.Elements[i].arglist[0])
            t *= coe
            t = int(t)
            affFile.Elements[i].arglist[0] = str(t)
        elif affFile.Elements[i].name == "arc":
            t1, t2 = float(affFile.Elements[i].arglist[0]), float(affFile.Elements[i].arglist[1])
            t1 *= coe
            t2 *= coe
            t1, t2 = int(t1), int(t2)
            affFile.Elements[i].arglist[0], affFile.Elements[i].arglist[1] = str(t1), str(t2)
            if len(affFile.Elements[i].follist) != 0:
                for j in range(len(affFile.Elements[i].follist)):
                    t = float(affFile.Elements[i].follist[j].arglist[0])
                    t *= coe
                    t = int(t)
                    affFile.Elements[i].follist[j].arglist[0] = str(t)
        elif affFile.Elements[i].name == "scenecontrol":
            tstart = float(affFile.Elements[i].arglist[0])
            tstart *= coe
            tstart = int(tstart)
            affFile.Elements[i].arglist[0] = str(tstart)
            if affFile.Elements[i].arglist[1] == "enwidencamera" or affFile.Elements[i].arglist[1] == "enwidenlanes":
                tduration = float(affFile.Elements[i].arglist[2])
                tduration *= coe
                tduration *= 100
                tduration =  int(tduration)
                tduration /= 100
                affFile.Elements[i].arglist[2] = str(tduration)

    for k in range(len(affFile.TimingGroups)):
        for i in range(len(affFile.TimingGroups[k].Elements)):
            if affFile.TimingGroups[k].Elements[i].name == "timing":
                t, bpm = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
                t *= coe
                bpm *= speed
                t = int(t)
                bpm = float(int(100 * bpm)/100)
                affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t), str(bpm)
            elif affFile.TimingGroups[k].Elements[i].name == "hold":
                t1, t2 = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
                t1 *= coe
                t2 *= coe
                t1, t2 = int(t1), int(t2)
                affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t1), str(t2)
            elif affFile.TimingGroups[k].Elements[i].name == "":
                t = float(affFile.TimingGroups[k].Elements[i].arglist[0])
                t *= coe
                t = int(t)
                affFile.TimingGroups[k].Elements[i].arglist[0] = str(t)
            elif affFile.TimingGroups[k].Elements[i].name == "arc":
                t1, t2 = float(affFile.TimingGroups[k].Elements[i].arglist[0]), float(affFile.TimingGroups[k].Elements[i].arglist[1])
                t1 *= coe
                t2 *= coe
                t1, t2 = int(t1), int(t2)
                affFile.TimingGroups[k].Elements[i].arglist[0], affFile.TimingGroups[k].Elements[i].arglist[1] = str(t1), str(t2)
                if len(affFile.TimingGroups[k].Elements[i].follist) != 0:
                    for j in range(len(affFile.TimingGroups[k].Elements[i].follist)):
                        t = float(affFile.TimingGroups[k].Elements[i].follist[j].arglist[0])
                        t *= coe
                        t = int(t)
                        affFile.TimingGroups[k].Elements[i].follist[j].arglist[0] = str(t)
            elif affFile.TimingGroups[k].Elements[i].name == "scenecontrol":
                tstart = float(affFile.TimingGroups[k].Elements[i].arglist[0])
                tstart *= coe
                tstart = int(tstart)
                affFile.TimingGroups[k].Elements[i].arglist[0] = str(tstart)
                if affFile.TimingGroups[k].Elements[i].arglist[1] == "enwidencamera" or affFile.TimingGroups[k].Elements[i].arglist[1] == "enwidenlanes":
                    tduration = float(affFile.TimingGroups[k].Elements[i].arglist[2])
                    tduration *= coe
                    tduration *= 100
                    tduration =  int(tduration)
                    tduration /= 100
                    affFile.TimingGroups[k].Elements[i].arglist[2] = str(tduration)
    return affFile

def module_main():
    filePath = input("file path: ")
    speed = float(input("speed: "))
    saveTo = input("save name: ")

    affString = ""

    with open(filePath, "r", encoding="utf-8") as f:
        affString = f.read()

    affFile = AffFile()
    affFile.load(affString)

    affFile = make_speed(affFile, speed)

    with open(f"{saveTo}.aff", "w+", encoding="utf-8") as f:
        f.write(affFile.toString())

if __name__ == "__main__":
    module_main()
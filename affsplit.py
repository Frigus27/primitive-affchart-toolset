from afflex import AffFile, AffElement, AffTimingGroup
import math
import copy

filePath = input("file path: ")


affString = ""

with open(filePath, "r", encoding="utf-8") as f:
    affString = f.read()

affFile = AffFile()
affFile.load(affString)
affFile.TimingPointDensityFactor = str(int(affFile.TimingPointDensityFactor))
affFile.AudioOffset = str(int(affFile.AudioOffset))

def parseArc(arc: AffElement):
    if (arc.name != "arc"):
        raise ValueError()
    
    arctaps = [int(e.arglist[0]) for e in arc.follist]

    return {
        "time": {
            "start": int(arc.arglist[0]),
            "end": int(arc.arglist[1]),
        },
        "posStart": {
            "x": float(arc.arglist[2]),
            "y": float(arc.arglist[5]),
        },
        "posEnd": {
            "x": float(arc.arglist[3]),
            "y": float(arc.arglist[6]),
        },
        "easing": arc.arglist[4],
        "color": int(arc.arglist[7]),
        "hitSound": arc.arglist[8],
        "isTrace": (arc.arglist[9] == "true"),
        "arctapTime": arctaps
    }

def buildArc(arcDict) -> AffElement:
    return AffElement(
        name = "arc",
        argument_list = [
            "{}".format(arcDict["time"]["start"]),
            "{}".format(arcDict["time"]["end"]),
            "{:.2f}".format(arcDict["posStart"]["x"]),
            "{:.2f}".format(arcDict["posEnd"]["x"]),
            arcDict["easing"],
            "{:.2f}".format(arcDict["posStart"]["y"]),
            "{:.2f}".format(arcDict["posEnd"]["y"]),
            "{}".format(arcDict["color"]),
            arcDict["hitSound"],
            "{}".format(arcDict["isTrace"]).lower(),
        ],
        followed_list = [
            AffElement("arctap", [f"{t}"], []) for t in arcDict["arctapTime"]
        ]
    )

def calcPosOffset(t_cur: int, t_arc_start: int, t_arc_end: int, arc_type: str) -> (float, float):
    '''
    calculate pos offset
    '''
    if t_arc_end == t_arc_start:
        return (0, 0)
    t = (t_cur - t_arc_start) / (t_arc_end - t_arc_start)
    if arc_type == "b":             #Bezier: x(t)=3t^2-2t^3, y(t)=t
        return ((3 * (t ** 2)) - (2 * (t ** 3)), t)
    elif arc_type == "s":           #Straight: x(t)=t, y(t)=t
        return (t, t)
    elif arc_type == "si":          #Sin in:x(t)=sin(pi*t/2), y(t)=t
        return (math.sin(math.pi * t / 2), t)
    elif arc_type == "so":          #Sin out:x(t)=1-cos(pi*t/2), y(t)=t
        return (1 - math.cos(math.pi * t / 2), t)
    elif arc_type == "sisi":        #Sin in Sin in
        return (math.sin(math.pi * t / 2), math.sin(math.pi * t / 2))
    elif arc_type == "siso":
        return (math.sin(math.pi * t / 2), 1 - math.cos(math.pi * t / 2))
    elif arc_type == "sosi":
        return (1 - math.cos(math.pi * t / 2), math.sin(math.pi * t / 2))
    elif arc_type == "soso":
        return (1 - math.cos(math.pi * t / 2), 1 - math.cos(math.pi * t / 2))
    else:
        raise NotImplementedError()

def genArctapArc(x: float, y: float, t: int) -> AffElement:
    return buildArc({
        "time": {
            "start": t,
            "end": t + 1,
        },
        "posStart": {
            "x": x,
            "y": y,
        },
        "posEnd": {
            "x": x,
            "y": y,
        },
        "easing": "s",
        "color": 2,
        "hitSound": "none",
        "isTrace": True,
        "arctapTime": [t]
    })

def splitArc(arc: AffElement):
    the_arc_dict = parseArc(arc)
    arctap_time_list = the_arc_dict["arctapTime"]
    the_arc_dict["arctapTime"] = []
    splitted_element_list = [buildArc(the_arc_dict)]
    for t in arctap_time_list:
        (x_off, y_off) =  calcPosOffset(t, the_arc_dict["time"]["start"], the_arc_dict["time"]["end"], the_arc_dict["easing"])
        x = x_off * (the_arc_dict["posEnd"]['x'] - the_arc_dict['posStart']['x']) + the_arc_dict['posStart']['x']
        y = y_off * (the_arc_dict["posEnd"]['y'] - the_arc_dict['posStart']['y']) + the_arc_dict['posStart']['y']
        splitted_element_list.append(genArctapArc(x, y, t))
    return splitted_element_list

new_list = []
# Base Group
for element in affFile.Elements:
    if element.name != "arc":
        new_list.append(element)
        continue
    arc_dict = parseArc(element)
    if len(arc_dict["arctapTime"]) == 0:
        new_list.append(element)
        continue
    splitted_list = splitArc(element)
    for splitted in splitted_list:
        new_list.append(splitted)

affFile.Elements = copy.deepcopy(new_list)

# Timing Group
for group in affFile.TimingGroups:
    new_list = []
    for element in group.Elements:
        if element.name != "arc":
            new_list.append(element)
            continue
        arc_dict = parseArc(element)
        if len(arc_dict["arctapTime"]) == 0:
            new_list.append(element)
            continue
        splitted_list = splitArc(element)
        for splitted in splitted_list:
            new_list.append(splitted)

    group.Elements = copy.deepcopy(new_list)


with open(f"{filePath}_produced.aff", "w+", encoding="utf-8") as f:
    f.write(affFile.toString())
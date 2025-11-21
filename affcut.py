import os
from afflex import AffFile, AffElement
import affsplit, afffrwrd

def alternate_music(ss: int, t: int):
    temp_ss = ss
    ss_ms = '%02d' % (temp_ss % 1000)
    temp_ss = temp_ss // 1000
    ss_s = '%02d' % (temp_ss % 60)
    temp_ss = temp_ss // 60
    ss_min = '%02d' % (temp_ss % 60)
    temp_ss = temp_ss // 60
    ss_h = '%02d' % (temp_ss)

    temp_t = t
    t_ms = '%02d' % (temp_t % 1000)
    temp_t = temp_t // 1000
    t_s = '%02d' % (temp_t % 60)
    temp_t = temp_t // 60
    t_min = '%02d' % (temp_t % 60)
    temp_t = temp_t // 60
    t_h = '%02d' % (temp_t)

    os.system(f"ffmpeg -i base.ogg -ss {ss_h}:{ss_min}:{ss_s}.{ss_ms} -t {t_h}:{t_min}:{t_s}.{t_ms} newbase.ogg")
    os.system("del base.ogg")
    os.system("ren newbase.ogg base.ogg")

def fix_timing(affFile: AffFile, first_timing: AffElement) -> AffFile:
    if len(affFile.Elements) == 0 or (len(affFile.Elements) >= 1 and affFile.Elements[0].name != "timing"):
        affFile.Elements.insert(0, first_timing)
    for k in range(len(affFile.TimingGroups)):
        if len(affFile.TimingGroups[k].Elements) == 0 or (len(affFile.TimingGroups[k].Elements) >= 1 and  affFile.TimingGroups[k].Elements[0].name != "timing"):
            affFile.TimingGroups[k].Elements.insert(0, first_timing)
    return affFile

def cut_file(affFile: AffFile, start: int, end: int) -> AffFile:
    forward = start
    backward = end

    affFile = affsplit.make_split(affFile)

    # save the first timing in order to fix
    first_timing = affFile.Elements[0]

    # Then filter
    affFile.Elements = list(filter(lambda x: (forward <= int(x.arglist[0]) and int(x.arglist[0]) <= backward) and not (x.name == "timing" and x.arglist[0] == "0"), affFile.Elements))

    for i in range(len(affFile.TimingGroups)):
        affFile.TimingGroups[i].Elements = list(filter(lambda x: (forward <= int(x.arglist[0]) and int(x.arglist[0]) <= backward) and not (x.name == "timing" and x.arglist[0] == "0"), affFile.TimingGroups[i].Elements))

    # forward
    affFile = afffrwrd.make_forward(affFile, forward)

    # fix first timing
    affFile = fix_timing(affFile, first_timing)
    
    return affFile


def module_main():
    affString = ""
    forward = int(input("begin time stamp: "))
    backward = int(input("end time stamp: "))
    interval = backward - forward

    with open("2.aff", "r", encoding="utf-8") as f:
        affString = f.read()

    affFile = AffFile()
    affFile.load(affString)
    affFile.TimingPointDensityFactor = str(int(affFile.TimingPointDensityFactor))
    affFile.AudioOffset = str(int(affFile.AudioOffset))

    affFile = cut_file(affFile, forward, backward)

    with open("produced.aff", "w+", encoding="utf-8") as f:
        f.write(affFile.toString())

    os.system("del 2.aff.bak")
    os.system("ren 2.aff 2.aff.bak")
    os.system("ren produced.aff 2.aff")

    alternate_music(forward, interval)

if __name__ == "__main__":
    module_main()

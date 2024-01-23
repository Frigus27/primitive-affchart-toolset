import json
import afflex
import copy
import os
from collections import OrderedDict

# get all available chart directories
dir_list = os.listdir(os.getcwd())
remove_list = []
for each in dir_list:
    if not os.path.isdir(each):
        remove_list.append(each)
    elif not os.path.exists(os.getcwd() + "\\" + each + "\\2.aff"):
        remove_list.append(each)
for each in remove_list:
    dir_list.remove(each)

name_list = copy.deepcopy(dir_list)
path_list = [ (os.getcwd() + "\\" + each + "\\2.aff") for each in dir_list ]

# get template
template_raw = ""
with open("template.json", "r", encoding="utf8") as f:
    template_raw = f.read()
song_list_template = json.loads(template_raw, object_pairs_hook=OrderedDict)


# process song list
song_list = {
    "songs": []
}

for i in range(len(path_list)):
    # get chart info
    bpm = 0
    bpm_str = ""
    if (os.path.exists(os.getcwd() + "\\" + name_list[i] + "\\bpm.txt")):
        with open(os.getcwd() + "\\" + name_list[i] + "\\bpm.txt", "r", encoding="utf8") as ff:
            bpm_str = ff.read()
        bpm = float(bpm_str)
    else:
        aff_file = afflex.AffFile()
        with open(path_list[i], "r", encoding="utf8") as f:
            aff_file.Elements = []
            aff_line = f.read()
        aff_file.load(aff_line)
        bpm_str = aff_file.Elements[0].arglist[1]
        bpm = float(bpm_str)

    # process new song list
    new_song_list = copy.deepcopy(song_list_template)
    new_song_list["id"] = name_list[i]
    new_song_list["title_localized"]["en"] = name_list[i]
    new_song_list["bpm"] = bpm_str
    new_song_list["bpm_base"] = bpm
    song_list["songs"].append(new_song_list)

with open("songlist.json", "w+", encoding="utf8") as f:
    f.write(json.dumps(song_list, sort_keys=False, indent=4, separators=(", ", ": "), ensure_ascii=False))
    
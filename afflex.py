class AffElement:
    def __init__(self, name, argument_list, followed_list = []):
        self.name = name
        self.arglist = argument_list
        self.follist = followed_list

    def toString(self):
        s = ''
        s += self.name
        s += '('
        for i in range(len(self.arglist)):
            if i!= 0:
                s += ','
            s += self.arglist[i]
        s+= ')'
        if len(self.follist) != 0:
            s += '['
            for j in range(len(self.follist)):
                if j != 0:
                    s += ','
                s += self.follist[j].toString()
            s+= ']'
        return s

class AffTimingGroup:
    def __init__(self, Attributes = [], Elements = []) -> None:
        self.Attributes = Attributes
        self.Elements = Elements
    
    def toString(self):
        s = "timinggroup("
        for i in range(len(self.Attributes)):
            if i != 0:
                s+="_"
            s += self.Attributes[i]
        s+= "){\n"
        for j in range(len(self.Elements)):
            s += "  " + self.Elements[j].toString() + ";\n"
        s += "};"
        return s

# only inplemented used functions
def lex_main_line(s):
    # pre-process
    if s[-1] == ';':
        s = s[:-1]
    
    # separate the main part and the followed part, e.g. arctaps
    main_part = ''
    followed_part = ''
    has_followed = True
    idx = s.rfind('[')
    if idx == -1:
        main_part = s
        has_followed = False
    else:
        main_part = s[:idx]
        followed_part = s[idx+1:-1]
    
    # process main part
    name = ''
    arg_list = []
    arg_list_string = ''
    jdx = main_part.rfind('(')
    if jdx == 0:
        # tap
        arg_list_string = main_part[1:-1]
    else:
        # others
        name = main_part[:jdx]
        arg_list_string = main_part[jdx+1:-1]
    arg_list = arg_list_string.split(',')

    # process followed part
    # Note: used simplified procedure. Will change if 616 changed its usage
    followed_list = []
    if has_followed:
        followed_list_raw = followed_part.split(',')
        for each in followed_list_raw:
            followed_list.append(lex_main_line(each))
    
    return AffElement(name, arg_list, followed_list)

def lex_timing_group(s):
    if not "timinggroup" in s:
        raise ValueError()
    
    # handle pararmeters
    idxbl = s.find("(")
    idxbr = s.find(")")
    parameters = s[idxbl+1:idxbr]
    parameters_list = parameters.split("_")

    # handle main code
    idx_code_start = s.find("{")
    idx_code_end = s.find("}") - 2
    main_code = s[idx_code_start+1:idx_code_end]
    processed_code = main_code.replace(" ", "").replace("\n", "")
    main_code_list_str = processed_code.split(";")
    main_code_list = []
    for each in main_code_list_str:
        main_code_list.append(lex_main_line(each))
    
    return AffTimingGroup(parameters_list, main_code_list)

class AffFile:
    def __init__(self, AudioOffset='0', TimingPointDensityFactor='1', Elements=[], TimingGroups = []):
        self.AudioOffset = AudioOffset
        self.TimingPointDensityFactor = TimingPointDensityFactor
        self.Elements = Elements
        self.TimingGroups = TimingGroups

    def set(self, AudioOffset='0', TimingPointDensityFactor='1', Elements=[], TimingGroups = []):
        self.AudioOffset = AudioOffset
        self.TimingPointDensityFactor = TimingPointDensityFactor
        self.Elements = Elements
        self.TimingGroups = TimingGroups

    def load(self, AffStringLine):
        t=0
        self.set()
        headers = []
        elements = []
        timinggroups = []

        # pre-process the timinggroup
        timinggroupSplitted = AffStringLine.split("timinggroup")
        for i in range(1, len(timinggroupSplitted)):
            news = "timinggroup" + timinggroupSplitted[i]
            timinggroups.append(lex_timing_group(news))
        self.TimingGroups = timinggroups

        AffStringLines = timinggroupSplitted[0].split("\n")
        for i in range(len(AffStringLines)):
            if AffStringLines[i] == '-':
                headers = AffStringLines[:i]
                elements = AffStringLines[i+1:]
                break
        if len(headers) == 1:
            self.AudioOffset = (headers[0].split(':')[1])
            self.TimingPointDensityFactor = '1'
        elif len(headers) == 2:
            self.AudioOffset = int((headers[0].split(':'))[1])
            self.TimingPointDensityFactor = int((headers[1].split(':'))[1])
        else:
            raise ValueError()
        
        for eachLine in elements:
            if len(eachLine) != 0:
                self.Elements.append(lex_main_line(eachLine))
                t+=1
        print(t)
        
    def toString(self) :
        s = "AudioOffset:" + self.AudioOffset + "\nTimingPointDensityFactor:" + self.TimingPointDensityFactor + "\n-\n"
        for eachEle in self.Elements:
            s += eachEle.toString() + ";\n"
        for eachTime in self.TimingGroups:
            s += eachTime.toString() + "\n"
        return s
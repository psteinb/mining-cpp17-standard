import re

def cpp_texlist(listoflines):

    value = []
    if not listoflines:
        return value

    srex = re.compile(r"\\.*Sec([0-9]*)\[(.*)\]\{(.*)\}*")
    irex = re.compile(r"\\impldef\{(.*)\}*")

    cnt = 0
    for line in listoflines:
        cnt += 1
        sres = srex.search(line)
        if sres:
            value.append( (cnt,line) )
            if not '}' in line:
                for li in listoflines[cnt-1:]:
                    value[-1][-1] += li
                    if '}' in li:
                        break
        ires = irex.search(line)
        if ires:
            value.append( (cnt,line) )

    return value

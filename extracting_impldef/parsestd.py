import re
from pathlib import Path

srex = re.compile(r"\\.{0,1}Sec([0-9]*)\[(.*)\]\{(.*)\}*")
irex = re.compile(r"\\impldef\{(.*)\}*")

def cpp_texlist(listoflines):
    """function that parses a .tex file from https://github.com/cplusplus/draft.git
    and extracts all section headings as well as all impldef statements into a flat list

    The return value contains tuples,
    tuple[0] ... line number (starting from 1) that matched the item
    tuple[1] ... the item matched (either a section heading or a impldef statement)
                 broken lines as in:
                 ```
                 some text before \impldef{with some important
                 content} appears here
                 ```
                 are appended to appear as '\impldef{with some important content}'
    """

    value = []
    if not listoflines:
        return value

    cnt = 0
    for line in listoflines:
        cnt += 1
        to_append = None
        sres = srex.search(line)
        if sres:
            to_append = line
            if not '}' in line:
                for li in listoflines[cnt:]:
                    if '}' in li:
                        to_append += li[:li.find('}')+1]
                        break
                    to_append += li
        ires = irex.search(line)
        if ires:
            to_append = line
            if not '}' in line:
                for li in listoflines[cnt:]:
                    if '}' in li:
                        to_append += li[:li.find('}')+1]
                        break
                    to_append += li

        if to_append:
            to_append = to_append.replace('\n','')
            value.append((cnt, to_append))

    return value


def parse_texfile(texfile):

    texp = Path(texfile)
    if not texp.exists():
        print(f"{texfile} does not exist")
        return []

    tex_lines = open(texp).readlines()

    return cpp_texlist(tex_lines)

def collapse_sections(parsed_itemlist, filename, max_sections = 0):
    """ will return a list of impldef items which have the hierarchy of sections prefixed, for example

    [
    [(some.tex:1, '\rSec0[foo]{bar}'), (some.tex:5, '\rSec1[baz]{42}'), (some.tex:6, '\impldef{But what was the question?}') ],
    ...
    ]
    """
    value = []
    if not parsed_itemlist or len(parsed_itemlist) == 0:
        return value

    current_sections = []
    impldef = []
    for idx in range(len(parsed_itemlist)):

        item = parsed_itemlist[idx]
        new_item = (f"{filename}:{item[0]}", item[-1])
        # print("::",item)
        if not 'impldef' in item[-1].lower():
            sres = srex.search(item[-1])
            if sres:
                try:
                    lvl = int(sres.groups()[0])+1
                except Exception as ex:
                    print(f"unable to apply regex to {item}")
                    raise
            else:
                print(f"WARNING, skipping {item[-1]} due to failing {srex} unexpectedly")
                continue

            if lvl < len(current_sections):
                current_sections = current_sections[:lvl-1]
                current_sections.append(new_item)

            if lvl == len(current_sections):
                current_sections[-1] = new_item

            if lvl > len(current_sections):
                current_sections.append(new_item)

        else:
            impldef = current_sections
            if max_sections > 0:
                if max_sections <= len(current_sections):
                    impldef = impldef[:max_sections]
                else:
                    #padding
                    padding = max_sections - len(current_sections)
                    paditem = (f"{filename}:-1", "")
                    by = padding*[paditem]
                    impldef.extend(by)


            impldef.append(new_item)

            value.append(impldef)

    return value


def flat_generator(lst):

    for x in lst:

        if isinstance(x, list) or isinstance(x, tuple):
            for x in flat_generator(x):
                yield x
        else:
            yield x


def flatten(lst):

    value = list(flat_generator(lst))

    return value


def flatten_items(lst):

    value = []
    if not lst:
        return value

    for it in lst:
        value.append(list(flat_generator(it)))

    return value

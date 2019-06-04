
from TexSoup import TexSoup as texsoup, RArg, TexNode
from pathlib import Path
from tex2py import tex2py
import pytest


def replace_cpp_standard_sections(infile,ofile):

    latex_sections = ["chapter", "section", 1*"sub" + "section", 2*"sub" + "section", "paragraph"]

    fp = open(infile)
    tex_src = []
    nlines = 0
    for line in fp.readlines():

        if "rSec" in line:
            index = line.find("rSec")
            if index > -1:
                level = int(line[index+4])
                tex_src.append(line.replace(f"rSec{level}",latex_sections[level]))
        else:
            tex_src.append(line)

        nlines += 1

    op = open(ofile,"w")
    op.writelines(tex_src)

    return True


TEXPATH = Path("cpp17-excerpt.tex")
TEXPATH_filtered = Path("filtered-cpp17-excerpt.tex")

def test_num_exists():

    assert (TEXPATH).exists()
    assert (TEXPATH_filtered).exists()


def test_find_impldef_tex2py():

    fp = open(TEXPATH_filtered)

    toc = tex2py(fp.read())

    for s in toc.branches:
        assert s.name
        print(s.name)


def test_wrapped_tex2py():

    fp = open(TEXPATH_filtered)

    content = [r"\documentclass[a4paper]{book}",r"\begin{document}"]
    content.extend(fp.readlines())
    content.append(r"\end{document}")
    toc = tex2py("\n".join(content))

    assert len(list(toc.chapters)) > 0
    assert len(list(toc.chapter.sections)) > 0
    res = []
    for s in toc.chapter.sections:
        print(toc.chapter.source.args, "::", s.source.args, len(res))
        branchid = 0
        for br in s.branches:
            if isinstance(br.source, TexNode) and br.source.count("impldef"):
                print(branchid)
                cands = br.source.find_all("impldef")
                for c in cands:
                    res.append( (s.source.args[-1],c.args[-1]) )

            branchid += 1
        assert branchid > 0
    assert len(res) > 0
    assert len(res) == 5


def test_parse_texsoup():
    fpath = TEXPATH
    with open(str(fpath)) as f:
        data = f.read()
        toc = texsoup(data)
        assert hasattr(toc,"sections")



@pytest.fixture
def conversions():
    fpath = TEXPATH
    f = open(str(fpath))
    return texsoup(f)

def test_find_sections(conversions):

    assert hasattr(conversions,"item")

    assert hasattr(conversions,"rSec")
    assert conversions.rSec0

    sections = conversions.find_all("rSec")

    any_titles = [ item.name for item in sections ]

    assert len(any_titles) == 0

    sections = conversions.find_all("rSec0")

    titles_sec0 = [ item.args for item in sections ]

    assert len(titles_sec0) == 1

    assert "Standard" in titles_sec0[0][-1]

    sections = conversions.find_all("rSec1")

    titles_sec1 = [ item.args for item in sections ]

    assert len(titles_sec1) > 0
    assert len(titles_sec1) > len(titles_sec0)


def test_find_impldef(conversions):

    impldefs = conversions.find_all("impldef")
    loci = [ item.name for item in impldefs ]

    assert len(loci) == 5


def test_find_impldef_section(conversions):

    impldefs = conversions.find_all("impldef")

    for ids in impldefs:
        assert ids.parent

        neighborhood = [ item for item in ids.parent.children ]
        assert len(neighborhood) > 0
        neighborhood2 = [ item for item in ids.parent.parent.children ]
        assert len(neighborhood2) > 1

def test_find_impldef_section(conversions):

    latex_sections = ["chapter", "section", 1*"sub" + "section", 2*"sub" + "section", "paragraph"]

    fp = open(TEXPATH)
    tex_src = []
    nlines = 0
    for line in fp.readlines():

        if "rSec" in line:
            index = line.find("rSec")
            if index > -1:
                level = int(line[index+4])
                tex_src.append(line.replace(f"rSec{level}",latex_sections[level]))
        else:
            tex_src.append(line)

        nlines += 1

    assert len(tex_src) == nlines

    souped = texsoup(tex_src)
    assert souped.chapter
    assert souped.chapter.args
    assert souped.chapter.descendants

    assert souped.section.args

    sec_gen = souped.find_all("section")
    secs = [s for s in sec_gen]
    assert len(secs) > 0


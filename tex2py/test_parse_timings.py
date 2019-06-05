
from TexSoup import TexSoup as texsoup, RArg, TexNode
from pathlib import Path
from tex2py import tex2py
from parsestd import cpp_texlist
import pytest

TEXPATH = Path("cpp17-excerpt.tex")
TEXPATH_filtered = Path("filtered-cpp17-excerpt.tex")

def test_num_exists():

    assert (TEXPATH).exists()
    assert (TEXPATH_filtered).exists()


def test_find_impldef_tex2py():

    fp = open(TEXPATH_filtered)

    toc = tex2py(fp.read())

    assert len(list(toc.branches)) > 0


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


def test_parse_texsoup():
    fpath = TEXPATH
    with open(str(fpath)) as f:
        data = f.read()
        toc = texsoup(data)
        assert hasattr(toc,"sections")


def test_runtime_texsoup(benchmark):

    def parse(infile):
        with open(str(infile)) as f:
            data = f.read()
            toc = texsoup(data)
            return toc

    benchmark(parse,TEXPATH)

def test_runtime_tex2py(benchmark):

    def parse(infile):
        with open(str(infile)) as f:
            data = f.read()
            toc = tex2py(data)
            return toc

    benchmark(parse,TEXPATH)

def test_runtime_parsestd(benchmark):

    def parse(infile):
        with open(str(infile)) as f:
            data = f.readlines()
            toc = cpp_texlist(data)
            return toc

    benchmark(parse,TEXPATH)

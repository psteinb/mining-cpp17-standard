import re
from pathlib import Path
import pytest
from parsestd import cpp_texlist, collapse_sections, flatten_items

TEXPATH = Path("cpp17-excerpt.tex")
TEXPATH_filtered = Path("filtered-cpp17-excerpt.tex")
tstr1 = r'\rSec0[conv]{Standard conversions}'
tstr2 = r'\xxx[conv]{Standard conversions}'
tstr3 = r'''\rSec3[conv]{Standard
    conversions on a newline}'''

@pytest.fixture
def tex_lines():
    return open(str(TEXPATH)).readlines()


def test_lines_read(tex_lines):

    assert len(tex_lines) > 0


def test_sections_full_re(tex_lines):

    rex = re.compile("\\.*Sec[0-9]\[.*\]\{.*\}")

    assert len(rex.findall(tstr1)) > 0

    res = rex.search(tstr1)
    assert not isinstance(res, type(None))
    assert res.start() > -1
    assert res.end() == len(tstr1)

    res = rex.search(tstr2)

    assert not res

    res = rex.search(tstr3)

    assert not res


def test_sections_grouped_re(tex_lines):

    rex = re.compile("\\.*Sec([0-9])\[(.*)\]\{(.*)\}*")

    res = rex.search(tstr1)
    assert res
    assert res.groups()
    assert len(res.groups()) == 3
    assert res.groups()[0] == '0'
    assert 'conv' in res.groups()[1]
    assert 'Standard' in res.groups()[2]

    res = rex.search(tstr2)
    assert not res

    res = rex.search(tstr3)
    assert res
    assert res.groups()
    assert len(res.groups()) == 3
    assert res.groups()[0] == '3'
    assert 'conv' in res.groups()[1]
    assert 'Standard' in res.groups()[2]


def test_cpp_tex():

    alist = [tstr1, tstr2, tstr3]
    res = cpp_texlist(alist)

    assert len(res) > 0
    assert res[0][-1] == tstr1
    assert len(res) == 2
    assert res[-1][0] == 3
    assert 'rSec3' in res[-1][-1]
    assert 'newline' in res[-1][-1]


def test_cpp_textlist_std(tex_lines):

    digest = cpp_texlist(tex_lines)

    assert len(digest) > 0

    secs = [ item for item in digest if 'Sec' in item[-1] ]
    idef = [ item for item in digest if 'impldef' in item[-1] ]

    assert len(idef) == 5
    assert len(secs) > 0
    assert len(secs) == 16


def test_cpp_textlist_merge(tex_lines):

    digest = cpp_texlist(tex_lines)

    assert len(digest) > 0

    collapsed = collapse_sections(digest, TEXPATH)

    assert collapsed
    assert len(collapsed) > 0
    assert len(collapsed[0]) > 0
    assert len(collapsed[0]) == 3
    assert len(collapsed[-1]) == 3
    assert len(collapsed[2]) == 3
    assert 'floating-point conversion' in collapsed[2][-1][-1]

    padded = collapse_sections(digest, TEXPATH, 4)
    assert padded
    assert len(padded) > 0
    assert len(padded[0]) > 0
    assert len(padded[0]) == 5
    assert 'floating-point conversion' in padded[2][-1][-1]


def test_flatten_items(tex_lines):

    digest = cpp_texlist(tex_lines)

    assert len(digest) > 0

    collapsed = collapse_sections(digest, TEXPATH)

    assert collapsed
    assert len(collapsed) > 0

    flat = flatten_items(collapsed)

    assert flat
    assert len(flat) > 0
    for fl in flat:
        for it in fl:
            assert not isinstance(it, tuple)

    print("\n", flat[-1])


def test_flat_generator():
    list_of_lists = [[180.0, 1, 2, 3], [173.8], [164.2], [156.5], [147.2],
                     [138.2]]
    nested = [[180.0, 1, 2, 3], [173.8, list(range(10, 5, -1))], [164.2],
              [156.5], [147.2], [138.2]]

    res = flatten_items(list_of_lists)
    assert isinstance(res, list)
    for it in res:
        assert isinstance(it, list)

    res = flatten_items(nested)
    assert isinstance(res, list)
    assert isinstance(res[0], list)
    assert not isinstance(res[1][1], list)


def test_intertools_chain():

    list_of_lists = [[180.0, 1, 2, 3], [173.8], [164.2], [156.5], [147.2],
                     [138.2]]
    nested = [[180.0, 1, 2, 3], [173.8, list(range(10, 5, -1))], [164.2],
              [156.5], [147.2], [138.2]]

    from itertools import chain
    res = list(chain.from_iterable(list_of_lists))
    assert isinstance(res, list)
    for it in res:
        assert not isinstance(it, list)

    res = list(chain.from_iterable(nested))
    assert isinstance(res, list)
    assert isinstance(res[5], list) #should not be!

from tex2py import tex2py
from TexSoup import TexSoup as texsoup
from pathlib import Path

texpath = Path("/home/steinbac/development/c++-standard-draft/source")

def test_num_exists():

    assert (texpath / "conversions.tex").exists()

def test_parse_constructs():

    fpath = texpath / "conversions.tex"
    with open(str(fpath)) as f:
        data = f.read()
        toc = tex2py(data)
        assert hasattr(toc,"sections")

def test_parse_texsoup():
    fpath = texpath / "conversions.tex"
    with open(str(fpath)) as f:
        data = f.read()
        toc = texsoup(data)
        assert hasattr(toc,"sections")

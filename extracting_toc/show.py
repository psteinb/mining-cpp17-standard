#!/usr/bin/env python3

#install pdfminer.six through `pip3 install --user pdfminer.six`
#for help see https://euske.github.io/pdfminer/programming.html
#or https://pdfminer-docs.readthedocs.io/programming.html

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal


# Open a PDF document.
fp = open('std.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
print_a = True

# Get the outlines of the document.
outlines = document.get_outlines()
interesting = []
for (level,title,dest,a,se) in outlines:
    if "random" in title:
        print(f"{level}  ==  {title}, {dest}, {a}, {se}")
        if print_a:
            print(a.objid,a.doc,type(a.doc))
            print_a = False
            interesting.append( (level,title,a.objid,a.doc) )
    else:
        continue
        print(level," :: ",title)

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
#device = PDFDevice(rsrcmgr)

# Create a PDF interpreter object.
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)

for item in interesting:
    page_gen = PDFPage.create_pages(item[-1])

    npages = 0
    page_text = []
    for page in page_gen:
        interpreter.process_page(page)
        layout = device.get_result()
        npages += 1
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                page_text.append(element.get_text())

    print("## ",item[:2],npages,len(page_text))

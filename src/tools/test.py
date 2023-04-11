# %%
from GrobidOutputReader import GrobidOutputReader
import os

# %%
# test the GrobidOutputReader
# create a GrobidOutputReader object
grobid_reader = GrobidOutputReader()
# %%
result = grobid_reader.XMLtoText(r'C:\Users\norouzin\Desktop\Codes\src-ssc-knowdelge-graph\src\tools\ENG00012.tei.xml', divide_by_headline=False)
# %%
print(result)
# %%

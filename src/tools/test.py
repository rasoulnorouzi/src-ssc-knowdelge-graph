# %%
from GrobidOutputReader import GrobidOutputReader
import os

# %%
# test the GrobidOutputReader
# create a GrobidOutputReader object
grobid_reader = GrobidOutputReader()
# %%
result = grobid_reader.XMLtoText('src\tools\ENG00010.tei.xml', divide_by_headline=False)
# %%
print(result)
# %%

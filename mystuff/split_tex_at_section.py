import sys, os
from texsplitter import texsplitter

basefilename = sys.argv[1]
if basefilename.endswith(".tex"):
    # Stem fully qualified basefilename, so that only one extension will exist in outfiles
    basefilename = basefilename[:-4]
print("Basefilename:", basefilename)

# subsection = texsplitter(basefilename, "\\subsection{", "subsection")
# section    = texsplitter(basefilename, "\\section{", "section", subsection)

section = texsplitter(basefilename, "\\section{", "section")

with open(basefilename + ".tex") as f:
    section.process(f.readlines())

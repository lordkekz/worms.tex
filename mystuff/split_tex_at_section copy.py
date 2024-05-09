import sys, os

basefilename = sys.argv[1]
basefilename_stemmed = basefilename
if basefilename.endswith(".tex"):
    # Stem fully qualified basefilename, so that only one extension will exist in outfiles
    basefilename_stemmed = basefilename[:-4]
else:
    # Append extension for compatibility with latex compiler arguments
    basefilename = basefilename+".tex"
print("Basefilename:", basefilename)
print("Stemmedname: ", basefilename_stemmed)

with open(basefilename) as basefile:
    i = -1
    preamble = []
    outfile = None
    lines_in_section = 0
    for line in basefile.readlines():
        if "\\section{" in line:
            if outfile != None:
                # end current file
                outfile.write("\\end{document}")
                outfile.close()
                if lines_in_section <= 1:
                    os.rename(outfile.name, outfile.name+".EMPTYSECTION")
            i += 1
            outfile = open(f"{basefilename_stemmed}_{i+1}.section.tex", mode="w")
            outfile.writelines(preamble)
            outfile.write("\setcounter{section}{"+str(i)+"}\n")
            lines_in_section = 0
        if i < 0:
            # Walk through preamble
            preamble.append(line)
        else:
            # Write section content
            outfile.writelines(line)
            lines_in_section += 1
    outfile.close()

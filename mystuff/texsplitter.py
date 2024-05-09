from io import TextIOWrapper
import os
from typing import TextIO


class texsplitter:
    
    def __init__(self, basefilename: str, split_matcher: str, countername: str, post: "texsplitter | None" = None) -> None:
        self.splitmark = split_matcher
        self.countername = countername
        self.pre = None
        self.post = post
        if post is not None:
            post.pre = self
        self.basefilename = basefilename
        self.reset()

    def reset(self):
        self.counter = -1
        self.preamble = []
        self.outfile = None
        self.content_lines = 0
        if self.post is not None:
            self.post.reset()
        
    def process(self, lines):
        self.reset()
        for line in lines:
            self.process_line(line)
        self.outfile.close()
    
    def process_line(self, line: str):
        if self.splitmark in line:
            self.root().try_save_file()
            
            # Bubbling reset to post-splitters
            if self.post is not None:
                self.post.reset()
            
            # Bubbling file-initialization
            self.counter += 1
            self.root().init_file()

        if self.counter < 0:
            # Walk through preamble
            self.preamble.append(line)
        elif self.post is not None:
            # Recursive call
            self.post.process_line(line)
        else:
            # Write section content
            self.outfile.writelines(line)
            self.root().content_lines += 1
    
    def try_save_file(self) -> None:
        if self.outfile is None:
            return
        # end current file
        keep_file = self.write_preamble_if_uncalled()
        self.outfile.write("\\end{document}")
        self.outfile.close()
        if not keep_file:
            os.remove(self.outfile.name)
        elif self.content_lines <= 1:
            os.rename(self.outfile.name, self.outfile.name+".EMPTYSECTION")

    ### Returns True if the file can be kept.
    def write_preamble_if_uncalled(self) -> bool:
        if self.counter < 0 and len(self.preamble) == 0:
            return False
        elif self.counter < 0:
            self.outfile.writelines(self.preamble)
            return True
        elif self.post is not None:
            return self.post.write_preamble_if_uncalled()
        else:
            return True

    def init_file(self, outfile: TextIOWrapper = None) -> None:
        if outfile is None:
            outfile = open(f"{self.basefilename}_{self.make_identifier()}.section.tex", mode="w")
        
        self.outfile = outfile
        self.outfile.writelines(self.preamble)
        if self.counter >= 0:
            self.outfile.write(f"\setcounter{{{self.countername}}}{{{self.counter}}}\n")
        self.content_lines = 0

        # Bubbling to post-splitters
        if self.post is not None:
            self.post.init_file(outfile)

    def root(self) -> "texsplitter":
        return self if self.pre is None else self.pre

    def make_identifier(self) -> str:
        if self.post is None:
            return str(self.counter+1)
        return f"{self.counter+1}_{self.post.make_identifier()}"

#!/usr/bin/env python3
"""Make os_midterm_cheatsheet_compact.html from os_midterm_cheatsheet.html
by appending denser print CSS (same content, fewer pages).
Render: node render_pdf.js os_midterm_cheatsheet_compact.html os_midterm_cheatsheet_compact.pdf"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
FS = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0   # body font size (pt)
CSS = f"""
@page{{ size: Letter; margin: 0.28in 0.3in; }}
body{{ font-size:{FS}pt; line-height:1.2; }}
h1{{ font-size:11pt; }} .sub{{ font-size:{FS-0.4}pt; margin-bottom:3px; }}
.cols{{ column-gap:10px; }}
h2{{ font-size:{FS+1.2}pt; padding:1px 4px; margin:4px 0 2px; }}
h3{{ font-size:{FS+0.3}pt; margin:3px 0 1px; }}
p{{ margin:1px 0 2px; }} ul,ol{{ margin:1px 0 2px; padding-left:12px; }} li{{ margin:0; }}
pre{{ font-size:{FS-1.6}pt; line-height:1.13; padding:2px 3px; margin:1px 0 2px; }}
code{{ font-size:{FS-0.9}pt; padding:0 1px; }}
.q{{ padding:2px 4px; margin:3px 0; }}
table{{ font-size:{FS-0.8}pt; margin:1px 0 2px; }} th,td{{ padding:0 2px; }}
.gantt{{ font-size:{FS-1.4}pt; }} .ticks{{ font-size:{FS-1.8}pt; margin-bottom:2px; }}
.note{{ font-size:{FS-0.8}pt; }} .tag{{ font-size:{FS-1.7}pt; }}
"""
src = open(os.path.join(here, "os_midterm_cheatsheet.html")).read()
out = src.replace("</style>", CSS + "</style>", 1)
open(os.path.join(here, "os_midterm_cheatsheet_compact.html"), "w").write(out)
print("wrote os_midterm_cheatsheet_compact.html at", FS, "pt")

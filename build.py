#!/usr/bin/env python3
"""Rebuild index.html from "Whose Words.dc.html".

index.html is the self-contained deploy build: it embeds the whole DC source
("Whose Words.dc.html") as a JSON string inside <script type="__bundler/template">,
alongside the inlined runtime. Editing the source alone does NOT update the deployed
page — you must re-embed it. This script does exactly that, losslessly.

Usage:
    python3 build.py        # edit "Whose Words.dc.html" first, then run this, then commit
"""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
dc = open(os.path.join(here, "Whose Words.dc.html"), encoding="utf-8").read()
idx = open(os.path.join(here, "index.html"), encoding="utf-8").read()

tag = '<script type="__bundler/template">'
a = idx.find(tag) + len(tag)
b = idx.find("</script>", a)
if a < len(tag) or b == -1:
    raise SystemExit("Could not find the embedded template in index.html")
sa = idx.index('"', a)          # start of the JSON string literal
se = idx.rindex('"', a, b) + 1  # end of it

# Match the bundler's escaping: JSON string, then escape </ as </ so a
# </script> inside the template can't close the tag early.
new_embed = json.dumps(dc, ensure_ascii=False).replace("</", "<\\u002F")
idx2 = idx[:sa] + new_embed + idx[se:]
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(idx2)
print("index.html rebuilt from 'Whose Words.dc.html' (%d chars embedded)" % len(dc))

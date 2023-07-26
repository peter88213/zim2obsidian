#!/usr/bin/python3
"""Indent Markdown files exported with Zim.

- Loops through all subdirectories of a Zim notebook Markdown export.
- Replaces "&emsp;" with tabs. 
- Replaces "&nbsp;" with spaces. 

CAUTION:

All occurrences of "&emsp;" and "&nbsp;" are replaced. Not only those 
created with the subst_indent.py tool.

Usage:

1. Have Zim export the Notebook to Markdown (Export each page to a separate file). 
2. Copy this Python script into the export root directory. 
3. Start it by double clicking on it or from the console. 

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import glob
import os

print(f'*** Indent lines in "{os.getcwd()}" ***\n')

TAB = chr(9)
TAB_SUBST = '&emsp;'
SPACE = ' '
SPACE_SUBST = '&nbsp;'

for note in glob.iglob('**/*.md', recursive=True):
    # Read a file with ".md" extension.
    print(f'Processing "{note}" ...')
    with open(note, 'r', encoding='utf-8') as f:
        page = f.read()

    # Replace tab and space substitutes.
    page = page.replace(TAB_SUBST, TAB)
    page = page.replace(SPACE_SUBST, SPACE)

    # Save the processed file.
    with open(note, 'w', encoding='utf-8') as f:
        f.write(page)
print('\nDone.')

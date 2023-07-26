#!/usr/bin/python3
"""Substitute indentiations in a Zim notebook for Markdown export.

- Loops through all subdirectories of a Zim notebook.
- Replaces all leading tabs with "&emsp;". 
- Replaces all leading spaces with "&nbsp;". 

This is a preprocessor for Zim Markdown export. Since tabs and leading spaces
are not part of the Markdown specification, the Zim Markdown exporter may
discard them if not substituted with "safe" strings.
After export, you can restore the tabs and spaces with the indent_md.py tool.  

Usage:

1. Make a copy of your Zim notebook. 
2. Copy this Python script into the copy's root directory. 
3. Start it by double clicking on it or from the console. 

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import glob
import os

print(f'*** Substitute indentiations in "{os.getcwd()}" ***\n')

if input('CAUTION! The notebook will be modified. Continue(y/n)?') == 'y':
    HEADER = 'Content-Type: text/x-zim-wiki'
    TAB = chr(9)
    TAB_SUBST = '&emsp;'
    SPACE = ' '
    SPACE_SUBST = '&nbsp;'

    for note in glob.iglob('**/*.txt', recursive=True):
        # Read a file with ".txt" extension.
        with open(note, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines[0].startswith(HEADER):
            print(f'Converting "{note}" ...')
            newlines = []
            for line in lines:
                newline = []
                indent = True
                for c in line:
                    if indent:
                        if c == TAB:
                            newline.append(TAB_SUBST)
                        elif c == SPACE:
                            newline.append(SPACE_SUBST)
                        else:
                            newline.append(c)
                            indent = False
                    else:
                        newline.append(c)
                newlines.append(''.join(newline))

            # Save the processed file.
            with open(note, 'w', encoding='utf-8') as f:
                f.writelines(newlines)
    print('\nDone.')

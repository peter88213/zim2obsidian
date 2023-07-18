#!/usr/bin/python3
"""Rename Markdown files exported by Zim.

- Loops through all subdirectories of a Zim notebook Markdown export.
- Replaces the ".markdown" extension with ".md". 
- Fixes internal links to other pages.

Usage:

1. Have Zim export the Notebook to Markdown (Export each page to a separate file). 
2. Copy this Python script into the export root directory. 
3. Start it by double clicking on it or from the console. 

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)

Changelog:

v0.1.0 - Initial release.
"""

import glob
import os

print(f'*** Convert Zim .markdown export in "{os.getcwd()}" ***\n')

for note in glob.iglob('**/*.markdown', recursive=True):
    print(f'Converting "{note}" ...')

    # Read a file with ".markdown" extension.
    with open(note, 'r', encoding='utf-8') as f:
        text = f.read()
    filePath, fileExt = os.path.splitext(note)

    # Delete the original file.
    os.remove(note)

    # Fix local links.
    text = text.replace('.markdown)', '.md)')

    # Save the processed file with ".md" extension.
    with open(f'{filePath}.md', 'w', encoding='utf-8') as f:
        f.write(text)
print('\nDone.')

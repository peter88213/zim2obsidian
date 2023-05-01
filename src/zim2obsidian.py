#!/usr/bin/python3
"""Convert Zim Markdown export to Obsidian.

- Loops through all subdirectories of a Zim notebook Markdown export.
- Removes each note's first level heading and renames the file accordingly. 
- Converts internal links to other pages to Obsidian style.

Usage:

1. Export a Zim Notebook to Markdown (Export each page to a separate file).
2. Make sure the Markdown files have the ".md" extension. If not, run markdown2md.py first.
3. Copy this Python script into the export root directory. 
4. Start it by double clicking on it or from the console. 


Version 0.1.0
Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import glob
import os
import re

print(f'*** Convert Zim export in "{os.getcwd()}" to Obsidian ***\n')

# First run: Get the new note file names.

noteNames = {}

for noteFile in glob.glob('**/*.md', recursive=True):
    noteDir, oldName = os.path.split(noteFile)
    if noteDir:
        noteDir = f'{noteDir}/'
    print(f'Reading "{noteFile}" ...')

    # Read a note file.
    with open(noteFile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Generate a new file name from the note's heading.
    if lines[0].startswith('# '):
        newName = lines[0][2:].strip()

        # Remove forbidden characters.
        newName = newName.replace('"', '').replace("'", '').replace('?', '').replace('*', '')

        # Remove first heading.
        del lines[0]

        if newName != oldName:
            # Delete the original file.
            os.remove(noteFile)

            noteFile = f'{noteDir}{newName}.md'
            noteNames[oldName] = newName

        # Save the processed file under the new name.
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.writelines(lines)

# Second run: Adjust internal links.
for noteFile in glob.iglob('**/*.md', recursive=True):
    print(f'Adjusting links in "{noteFile}" ...')
    with open(noteFile, 'r', encoding='utf-8') as f:
        text = f.read()

    # Get all links.
    links = re.findall('\[.+?\]\(.+?\)', text)
    for link in links:
        for noteName in noteNames:
            if noteName in link:
                # Create an adjusted link.
                newLink = link.replace(noteName, noteNames[noteName])

                # Convert Markdown link to Obsidian link.
                newLink = re.sub('\[.+?\]', '', newLink)
                newLink = newLink.replace('(./', '[[')
                newLink = newLink.replace('(', '[[')
                newLink = newLink.replace(')', ']]')

                # Replace the Markdown links by Obsidian style links.
                text = text.replace(link, newLink)

    # Save the processed file.
    with open(noteFile, 'w', encoding='utf-8') as f:
        f.write(text)

print('\nDone.')

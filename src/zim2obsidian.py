#!/usr/bin/python3
"""Convert Zim Markdown export to Obsidian.

- Loops through all subdirectories of a Zim notebook Markdown export.
- Removes each note's first level heading and renames the file accordingly. 
- Replaces Setext-style headers with Atx-style headers.
- Converts horizontal rulers.
- Converts internal links to other pages to Obsidian style.

Usage:

1. Have Zim export the Notebook to Markdown (Export each page to a separate file). 
2. Make sure the Markdown files have the ".md" extension. If not, run markdown2md.py first.
3. Copy this Python script into the export root directory. 
4. Start it by double clicking on it or from the console. 

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)

Changelog:

v0.1.0 - Initial release.
v0.2.0 - Replace Setext-style headers with Atx-style headers.
v0.2.1 - Improve messaging.
v0.2.2 - Keep separators.
v0.3.0 - Convert horizontal lines.
v0.3.1 - Change the wording.
v0.3.2 - Fix a bug where the program may abort when a page is empty. 
v0.3.3 - Generously comment the code.
"""

import glob
import os
import re

print(f'*** Convert Zim export in "{os.getcwd()}" to Obsidian ***\n')

# First run: Get the new note file names.
noteNames = {}
# a dictionary; key: old note name, value: new note name (created from the heading)

for noteFile in glob.glob('**/*.md', recursive=True):
    # loop through all files with ".md" extension, include subdirectories

    noteDir, oldName = os.path.split(noteFile)
    if noteDir:
        noteDir = f'{noteDir}/'
    print(f'Reading "{noteFile}" ...')

    # Read a note file.
    with open(noteFile, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        # the original page's lines in a list

    # Generate a new file name from the note's heading.
    if lines[0].startswith('# '):
        newName = lines[0][2:].strip()

        # Remove forbidden characters.
        newName = newName.replace('"', '').replace("'", '').replace('?', '').replace('*', '')

        # Remove first heading.
        del lines[0]

        # Replace Setext-style headings with Atx-style headings; convert rulers.

        newLines = []
        # the processed page's lines in a list (to be populated during processing)

        previousLine = None
        # A first or second level heading is reformatted depending on the line that follows it.
        # For this, the previous line must be temporarily stored for processing.

        for  line in lines:

            # Loop through the original page's lines and create the processed page's lines.

            if line.startswith('=') and line.count('=') == len(line):
                # the actual line is a 1st level heading's underline

                print(f'Converting 1st level heading "{previousLine}" ...')
                previousLine = f'# {previousLine}'
                # adding a hashtag and a space to the previous line, discarding the actual line

            elif line.startswith('-') and line.count('-') == len(line):
                # the actual line is a 2nd level heading's underline

                print(f'Converting 2nd level heading "{previousLine}" ...')
                previousLine = f'## {previousLine}'
                # adding two hashtags and a space to the previous line, discarding the actual line

            elif line.startswith('*') and line.count('*') == len(line):
                # the actual line is a horizontal ruler (ZIM export style)

                print('Converting horizontal ruler ...')
                if previousLine is not None:
                    newLines.append(previousLine)
                    # adding the previous line to the list of processed lines

                previousLine = '---'
                # replacing the actual line with a standard Markdown horizontal ruler

            else:
                # nothing to convert ...

                if previousLine is not None:
                    newLines.append(previousLine)
                    # adding the previous line to the list of processed lines

                previousLine = line
                # storing the line temporarily, because the next line could be an "underline"

        if previousLine is not None:
            newLines.append(previousLine)
            # adding the very last line to the list of processed lines

        if newName != oldName:
            # Delete the original file.
            os.remove(noteFile)

            noteFile = f'{noteDir}{newName}.md'
            noteNames[oldName] = newName

        # Save the processed file under the new name.
        print(f'Writing "{noteFile}" ...')
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(newLines))

# Second run: Adjust internal links.
for noteFile in glob.iglob('**/*.md', recursive=True):
    # loop through all files with ".md" extension, include subdirectories

    print(f'Adjusting links in "{noteFile}" ...')
    with open(noteFile, 'r', encoding='utf-8') as f:
        text = f.read()
        # a string containing the whole page

    # Get all links.
    links = re.findall('\[.+?\]\(.+?\)', text)
    # a list with all Markdown links found in the page

    for link in links:
        # outer loop: links in the page

        for noteName in noteNames:
            # inner loop: the original file names of the exported notebook

            if noteName in link:
                # Create an adjusted link.
                newLink = link.replace(noteName, noteNames[noteName])
                # replacing the original file name with the new file name

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

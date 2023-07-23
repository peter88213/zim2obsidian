#!/usr/bin/python3
"""Convert Zim Markdown export to Obsidian.

- Loops through all subdirectories of a Zim notebook Markdown export.
- Optionally renames pages according to the names given by the top first level heading.
- Optionally removes each note's first line. 
- Optionally replaces Setext-style headers with Atx-style headers and converts horizontal rulers.
- Optionally converts internal links to other pages to Obsidian style.

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
v0.4.0 - Make it a module, ready for testing.
v0.4.1 - Extend the set of characters that filenames cannot contain.
v0.5.0 - Fix a bug where directories may be linked instead of pages. 
         Make the script configurable by modularizing the features.
         Handle links with braces in the filename.
         Make the script no longer rename pages.
v0.6.0 - Enable page renaming feature, now fixed.
         Also convert unlabeled links.
"""

import glob
import os
import re

# Configuration (to be changed by the user).

RENAME_PAGES = True
# if True, rename pages according to the names given by the top first level heading.

REMOVE_FIRST_LINE = True
# If True, remove the top heading inserted with Zim's default Markdown exporter template.

CHANGE_HEADING_STYLE = True
# If True, replace Setext-style headings with Atx-style headings; convert rulers.

REFORMAT_LINKS = True
# If True, change Markdown-style links to Obsidian-style links.


def rename_pages():
    """Rename pages according to the names given by the top first level heading."""

    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    # First run: Get the new note file names.
    noteNames = {}
    # a dictionary; key: old note name, value: new note name (created from the heading)

    for noteFile in glob.glob('**/*.md', recursive=True):
        # loop through all files with ".md" extension, include subdirectories

        noteDir, oldName = os.path.split(noteFile)
        if noteDir:
            noteDir = f'{noteDir}/'
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Generate a new file name from the note's heading.
        if lines[0].startswith('# '):
            newName = f'{lines[0][2:].strip()}.md'

            # Remove characters that filenames cannot contain.
            for c in FORBIDDEN_CHARACTERS:
                newName = newName.replace(c, '')

            if newName != oldName:
                print(f'Renaming "{noteFile}" ...')

                # Delete the original file.
                os.remove(noteFile)

                # Save the processed file under the new name.
                noteFile = f'{noteDir}{newName}'
                noteNames[oldName] = newName
                with open(noteFile, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

    # Second run: Adjust internal links.
    for noteFile in glob.glob('**/*.md', recursive=True):
        print(f'Adjusting links in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            page = f.read()
        for noteName in noteNames:
            links = re.findall(f'\[.+\]\((.*{noteName})\)', page)
            for oldLink in links:
                newLink = oldLink.replace(noteName, noteNames[noteName])
                print(f'{oldLink} --> {newLink}')
                page = page.replace(oldLink, newLink)
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write(page)


def remove_first_line():
    """Remove the first heading inserted with Zim's default Markdown exporter template."""
    for noteFile in glob.glob('**/*.md', recursive=True):
        print(f'Removing the first line of "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            del lines[0]
            with open(noteFile, 'w', encoding='utf-8') as f:
                f.writelines(lines)


def change_heading_style():
    """Replace Setext-style headings with Atx-style headings; convert rulers."""
    for noteFile in glob.glob('**/*.md', recursive=True):
        print(f'Reading "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            newLines = []

            previousLine = None
            # A first or second level heading is reformatted depending on the line that follows it.
            # For this, the previous line must be temporarily stored for processing.

            for  line in lines:
                if line.startswith('=') and line.count('=') == len(line):
                    print(f'Converting 1st level heading "{previousLine}" ...')
                    previousLine = f'# {previousLine}'
                elif line.startswith('-') and line.count('-') == len(line):
                    print(f'Converting 2nd level heading "{previousLine}" ...')
                    previousLine = f'## {previousLine}'
                elif line.startswith('*') and line.count('*') == len(line):
                    print('Converting horizontal ruler ...')
                    if previousLine is not None:
                        newLines.append(previousLine)
                    previousLine = '---'
                else:
                    # nothing to convert ...
                    if previousLine is not None:
                        newLines.append(previousLine)
                    previousLine = line
                    # storing the line temporarily, because the next line could be an "underline"
            if previousLine is not None:
                newLines.append(previousLine)
                # adding the very last line to the list of processed lines

            print(f'Writing "{noteFile}" ...')
            with open(noteFile, 'w', encoding='utf-8') as f:
                f.write('\n'.join(newLines))


def reformat_links():
    """Change Markdown-style links to Obsidian-style links."""
    for noteFile in glob.glob('**/*.md', recursive=True):
        print(f'Re-formatting links in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            page = f.read()
        page = re.sub('\[(.*)\]\((.+)\)', '[[\\2]]', page)
        page = page.replace('[[./', '[[')
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write(page)


def main():
    print(f'*** Convert Zim export in "{os.getcwd()}" to Obsidian ***\n')
    if RENAME_PAGES:
        rename_pages()
    if CHANGE_HEADING_STYLE:
        change_heading_style()
    if REMOVE_FIRST_LINE:
        remove_first_line()
    if REFORMAT_LINKS:
        reformat_links()
    print('\nDone.')


if __name__ == '__main__':
    main()


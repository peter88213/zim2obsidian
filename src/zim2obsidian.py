#!/usr/bin/python3
"""Post-process Zim Markdown export for use with Obsidian.

Loops through all subdirectories of a Zim notebook Markdown export and processes the pages.
For Details, see the README page on GitHub.

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
v0.6.1 - Refactor the code.
v0.6.2 - Speed up the script by rewriting only changed pages.
v0.6.3 - Optimize the code for low memory consumption.
         Improve messaging to obtain a full log.
v0.6.4 - Do not rename a page if another page with the new filename exists.
         Refactor the code for faster execution.
v0.6.5 - Make the change from v0.6.4 also work on non-Windows systems.
v0.6.6 - Secure the link adjustment against mistakes.
v0.7.0 - Convert highlighting.
v0.8.0 - Convert checkboxes.
v0.8.1 - Add messages for checkbox replacements.
v0.9.0 - Convert tags.
v0.10.0 - Convert checkboxes that are not in a list.
v0.10.1 - Fix a bug where changes in pages without first or second level headings are not saved.
v0.10.2 - Change the line breaks to Unix style.
v0.10.3 - No extra space before the Obsidian tag.
"""

import glob
import os
import re

# Configuration (to be changed by the user).

RENAME_PAGES = True
# if True, rename pages according to the names given by the top first level heading.

REMOVE_FIRST_LINE = True
# If True, remove the top heading inserted with Zim's default Markdown exporter template.

CHANGE_MARKDOWN_STYLE = True
# If True, convert Markdown formatting to Obsidian style.

REFORMAT_LINKS = True
# If True, change Markdown-style links to Obsidian-style links.


def rename_pages():
    """Rename pages according to the names given by the top first level heading.
    
    Note: Make sure to call this procedure before the page's first lines are removed.
    """

    # First run: Rename the pages and collect the new filenames.

    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    noteNames = {}
    # a dictionary; key: old note name, value: new note name (created from the heading)

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        noteDir, oldName = os.path.split(noteFile)
        if noteDir:
            noteDir = f'{noteDir}/'
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if lines[0].startswith('# '):
            # Generate a new file name from the note's heading.
            newName = f'{lines[0][2:].strip()}.md'

            # Remove characters that filenames cannot contain.
            for c in FORBIDDEN_CHARACTERS:
                newName = newName.replace(c, '')

            if newName != oldName:
                # Rename the file.
                newFile = f'{noteDir}{newName}'
                if not os.path.exists(newFile):
                    print(f'Renaming "{noteFile}" to "{newFile}" ...')
                    os.rename(noteFile, newFile)
                    noteNames[oldName] = newName
                else:
                    print(f'Cannot rename "{noteFile}" to "{newFile}" ...')

    # Second run: Adjust internal links.

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Adjusting links in "{noteFile}" ...')
        hasChanged = False
        with open(noteFile, 'r', encoding='utf-8') as f:
            page = f.read()
        for noteName in noteNames:
            links = re.findall(f'\[.+(\]\(.*{noteName}\))', page)
            for oldLink in links:
                newLink = oldLink.replace(noteName, noteNames[noteName])
                print(f'- Replacing {oldLink} with {newLink} ...')
                page = page.replace(oldLink, newLink)
                hasChanged = True
        if hasChanged:
            with open(noteFile, 'w', encoding='utf-8') as f:
                f.write(page)


def remove_first_line():
    """Remove the first heading inserted with Zim's default Markdown exporter template."""
    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Removing the first line of "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        del lines[0]
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.writelines(lines)


def change_md_style():
    """Convert Markdown formatting to Obsidian style.
    
    - Replace Setext-style headings with Atx-style headings
    - Convert rulers.
    - Convert highlighting.
    - Convert checkboxes.
    - Convert tags.
    """
    CHECKBOXES = {
                 '☐': '- [ ]',
                 '☑': '- [x]',
                 '☒': '- [c]',
                 '▷': '- [>]',
                 '◁': '- [<]',
                  }
    # replacement dictionary; key: Zim checkbox, value: Obsidian checkbox

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Reformatting headings in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        newLines = []
        previousLine = None
        # A first or second level heading is reformatted depending on the line that follows it.
        # For this, the previous line must be temporarily stored for processing.

        for  line in lines:
            if line.startswith('=') and line.count('=') == len(line):
                print(f'- Converting 1st level heading "{previousLine}" ...')
                previousLine = f'# {previousLine}'
            elif line.startswith('-') and line.count('-') == len(line):
                print(f'- Converting 2nd level heading "{previousLine}" ...')
                previousLine = f'## {previousLine}'
            elif line.startswith('*') and line.count('*') == len(line):
                print('- Converting horizontal ruler ...')
                if previousLine is not None:
                    newLines.append(previousLine)
                previousLine = '---'
            else:
                if previousLine is not None:
                    newLines.append(previousLine)

                # Convert checkboxes.
                for c in CHECKBOXES:
                    line = re.sub(f'(\* )*{c}', CHECKBOXES[c], line)

                # Convert highlighting.
                line = re.sub('__(.+?)__', '==\\1==', line)

                # Convert tags.
                if '@' in line:
                    print('- Converting tags ...')
                    line = re.sub('@(\S+?)', '#\\1', line)

                previousLine = line
                # storing the line temporarily, because the next line could be an "underline"
        if previousLine is not None:
            newLines.append(previousLine)
            # adding the very last line to the list of processed lines

        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(newLines))


def reformat_links():
    """Change Markdown-style links to Obsidian-style links."""
    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Reformatting links in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            page = f.read()
        page = re.sub('\[.*\]\((.+)\)', '[[\\1]]', page)
        page = page.replace('[[./', '[[')
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write(page)


def main():
    print(f'*** Convert Zim export in "{os.getcwd()}" to Obsidian ***\n')
    if RENAME_PAGES:
        rename_pages()
    if REMOVE_FIRST_LINE:
        remove_first_line()
    if CHANGE_MARKDOWN_STYLE:
        change_md_style()
    if REFORMAT_LINKS:
        reformat_links()
    print('\nDone.')


if __name__ == '__main__':
    main()


#!/usr/bin/python3
"""Post-process Zim Markdown export for use with Obsidian.

Loops through all subdirectories of a Zim notebook Markdown export and processes the pages.
For Details, see the README page on GitHub.

Suggested workflow:

1. Have Zim export the Notebook to Markdown (Export each page to a separate file). 
2. Make sure the Markdown files have the ".md" extension. If not, run markdown2md.py first.
3. Copy this Python script into the export root directory. 
4. Start zim2obsidian.py by double clicking on it or from the console. 

usage: zim2obsidian.py [-h] [-b] [-w] [-@]

options:
  -h, --help       show a help message and exit
  -b, --backticks  verbatim blocks and inline code are marked with backticks
  -w, --wikilinks  Convert Markdown links to wikilinks
  -@, --preserve_at  Do not convert Zim tags to Obsidian tags

Requires Python 3.9+
Copyright (c) 2025 Peter Triesberger
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
v0.4.1 - Extend the set of data that filenames cannot contain.
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
v0.10.4 - Rework reformat_links() to keep the custom link names.
v0.10.5 - Disable the conversion to wikilinks by default.
v0.11.0 - Escape spaces when renaming links.
          Remove leading "./" when renaming links.
v0.11.1 - Use a library function for escaping spaces in links.
v0.11.2 - Refactor the checkbox conversion code.
v0.11.3 - Bugfix: Exclude code blocks from zim2obsidian formatting
v0.11.4 - Fix bugs that show up at testing. Tests now o.k.
v0.11.5 - Exclude inline code from Markdown conversion.
v0.11.6 - Refactor the code.
v0.12.0 - Convert "verbatim" lines as exported by Zim. 
v0.13.0 - Make the "backticks" code conversion an option.
v0.13.1 - Provide an abbreviation for the "backticks" argument.
v0.13.2 - Preserving "@" inside words such as email addresses.
v0.13.3 - Refined regular expression to respect verbatim text.
v0.13.4 - Unquoting wikilinks.
v0.13.5 - Escaping regex special data in note names.
v0.14.0 - Improved wikilinks conversion, using a parser instead of regular expressions.
v0.14.1 - Refactored the wikilinks conversion for better performance.
v0.14.2 - Clearing the buffers in MdLinkParser.close().
v0.15.0 - New command line option: conversion of Markdown links to wikilinks.
v0.15.1 - Escaping opening square brackets that don't belong to links.
v0.15.2 - No longer converting links to wikilinks if the path is an URL.
"""

import glob
import os
import re
from urllib.request import pathname2url
from urllib.parse import unquote, urlparse

# Configuration (to be changed by the user).
RENAME_PAGES = True
# if True, rename pages according to the names given by the top first level heading.

REMOVE_FIRST_LINE = True
# If True, remove the top heading inserted with Zim's default Markdown exporter template.

CHANGE_MARKDOWN_STYLE = True
# If True, convert Markdown formatting to Obsidian style.


def rename_pages():
    """Rename pages according to the names given by the top first level heading.
    
    Note: Make sure to call this procedure before the page's first lines are removed.
    """
    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of data that filenames cannot contain

    #--- First run: Rename the pages and collect the new filenames.

    noteNames = {}
    # a dictionary; key: old note name, value: new note name (created from the heading)

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        noteDir, oldName = os.path.split(noteFile)
        if noteDir:
            noteDir = f'{noteDir}/'
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if lines and lines[0].startswith('# '):
            # Generate a new file name from the note's heading.
            newName = f'{lines[0][2:].strip()}.md'

            # Remove data that filenames cannot contain.
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

    #--- Second run: Adjust internal links.

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Adjusting links in "{noteFile}" ...')
        hasChanged = False
        with open(noteFile, 'r', encoding='utf-8') as f:
            page = f.read()
        for noteName in noteNames:
            escapedNoteName = re.escape(noteName)
            links = re.findall(fr'\[.+(\]\(.*{escapedNoteName}\))', page)
            for oldLink in links:
                newLink = oldLink.replace(noteName, pathname2url(noteNames[noteName])).replace('](./', '](')
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
        if lines:
            del lines[0]
            with open(noteFile, 'w', encoding='utf-8') as f:
                f.writelines(lines)


def change_md_style(backticks=False, preserveAt=False):
    """Convert Markdown formatting to Obsidian style.
    
    Optional arguments:
        backticks: bool -- If True, verbatim blocks and inline code are marked with backticks.
        
    - Replace Setext-style headings with Atx-style headings
    - Convert rulers.
    - Convert highlighting.
    - Convert checkboxes.
    - Convert tags.    
    """
    CHECKBOXES = {
                 '☐': '[ ]',
                 '☑': '[x]',
                 '☒': '[c]',
                 '▷': '[>]',
                 '◁': '[<]',
                  }
    # replacement dictionary; key: Zim checkbox, value: Obsidian checkbox

    CODE_BLOCK_MARKER = '```'
    # lines that start with this string will toggle the "code block mode"

    INLINE_CODE_MARKER = '`'
    # inline code is enclosed with this string

    def convert_md(text):
        """Return a converted string."""

        #--- Escape opening square brackets that don't belong to links.
        text = re.sub(r'(\[.*?\]\s)', r'\\\1', text)
        text = re.sub(r'\\\\(\[.*?\]\s)', r'\\\1', text)
        # undoing the substitution if the bracket was already escaped

        #--- Convert checkboxes.
        for c in CHECKBOXES:
            text = re.sub(fr'(\* )*{c}', f'- {CHECKBOXES[c]}', text)

        #--- Convert highlighting.
        text = re.sub('__(.+?)__', '==\\1==', text)

        #--- Convert tags.
        if not preserveAt and '@' in text:
            print('- Converting tags ...')
            text = re.sub(r'(\B)@{1}(\S+?)', '\\1#\\2', text)

        return text

    # Loop through all files with the ".md" extension, including subdirectories.
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Reformatting headings in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        newLines = []
        previousLine = None
        # A first or second level heading is reformatted depending on the line that follows it.
        # For this, the previous line must be temporarily stored for processing.

        isCodeblock = False
        # "code block mode" indicator

        for  line in lines:

            if line.startswith('=') and line.count('=') == len(line):

                #--- Convert 1st level heading.
                print(f'- Converting 1st level heading "{previousLine}" ...')
                previousLine = f'# {previousLine}'

            elif line.startswith('-') and line.count('-') == len(line):

                #--- Convert 2nd level heading.
                print(f'- Converting 2nd level heading "{previousLine}" ...')
                previousLine = f'## {previousLine}'

            elif line.startswith('*') and line.count('*') == len(line):

                #--- Convert horizontal ruler.
                print('- Converting horizontal ruler ...')
                if previousLine is not None:
                    newLines.append(previousLine)
                previousLine = '---'

            elif backticks:

                # Code blocks and inline code are marked with backticks.
                if line.startswith(CODE_BLOCK_MARKER):
                    isCodeblock = not isCodeblock
                    # toggling the "code block mode"

                if previousLine is not None:
                    newLines.append(previousLine)

                if not isCodeblock:

                    # Exclude inline code from conversion.
                    processedChunks = []
                    chunks = line.split(INLINE_CODE_MARKER)
                    for i, chunk in enumerate(chunks):
                        if i % 2:
                            processedChunks.append(chunk)
                            # chunk is considered inline code
                        else:

                            #--- Convert regular Markdown text.
                            processedChunks.append(convert_md(chunk))

                    line = INLINE_CODE_MARKER.join(processedChunks)
                previousLine = line
                # storing the line temporarily, because the next line could be an "underline"

            else:

                # Code blocks are indented with tabs.
                if previousLine is not None:
                    newLines.append(previousLine)

                if not isCodeblock:
                    if line.startswith('\t'):
                        # indented line means codeblock
                        newLines.append(CODE_BLOCK_MARKER)
                        # opening an Obsidian code block
                        isCodeblock = True
                elif not line.startswith('\t'):
                        newLines.append(CODE_BLOCK_MARKER)
                        # closing an Obsidian code block
                        isCodeblock = False

                if not isCodeblock:
                    line = convert_md(line)

                previousLine = line
                # storing the line temporarily, because the next line could be an "underline"

        if previousLine is not None:
            newLines.append(previousLine)
            # adding the very last line to the list of processed lines

        with open(noteFile, 'w', encoding='utf-8') as f:
            f.write('\n'.join(newLines))


class MdLinkParser:
    """Parser implementing a state machine for Markdown link conversion."""
    BODY = 0
    DESC = 1
    LINK = 2
    ADDRESS = 3

    def __init__(self):
        self.markup = {
            '[': self.handle_desc_start,
            ']': self.handle_desc_end,
            '(': self.handle_addr_start,
            ')': self.handle_addr_end,
        }
        self.results = []
        # list of characters and strings
        self.descBuffer = []
        # list of characters, buffering the read-in link description
        self.addrBuffer = []
        # list of characters, buffering the read-in link address
        self.state = self.BODY

    def to_wikilinks(self, text):
        """Return text with Markdown links converted into wikilinks.
        
        If addr is not an external URL, the coversion goes as follows:
        [desc](addr) --> [[addr|desc]]            
        """
        self.reset()
        self.feed(text)
        self.close()
        return ''.join(self.results)

    def reset(self):
        """Reset the instance. Loses all unprocessed data."""
        self.results.clear()
        self.descBuffer.clear()
        self.addrBuffer.clear()
        self.state = self.BODY

    def feed(self, data):
        """Feed some text to the parser."""
        for c in data:
            self.markup.get(c, self.handle_data)(c)

    def handle_desc_start(self, c):
        if self.state == self.BODY:
            self.state = self.DESC
        else:
            self.handle_data(c)

    def handle_desc_end(self, c):
        if self.state == self.DESC:
            self.state = self.LINK
        else:
            self.handle_data(c)

    def handle_addr_start(self, c):
        if self.state == self.LINK:
            self.state = self.ADDRESS
        else:
            self.handle_data(c)

    def handle_addr_end(self, c):
        if self.state == self.ADDRESS:
            if self.addrBuffer:
                addrStr = ''.join(self.addrBuffer)
                if urlparse(addrStr).scheme:

                    # The address is an external URL:
                    # Restore the original link.
                    self.results.append('[')
                    self.results.extend(self.descBuffer)
                    self.results.append('](')
                    self.results.append(addrStr)
                    self.results.append(')')

                else:
                    # Create a wikilink with address and description.
                    addrStr = addrStr.removeprefix('./')
                    self.results.append('[[')
                    addrStr = unquote(addrStr)
                    self.results.append(addrStr)
                    if self.descBuffer:
                        self.results.append('|')
                        self.results.extend(self.descBuffer)
                    self.results.append(']]')

            else:
                # No explicit address given:
                # Convert the description into an internal address
                # and create a wikilink.
                self.results.append('[[')
                addrStr = ''.join(self.descBuffer)
                addrStr = addrStr.replace(':', '/')
                addrStr = unquote(addrStr)
                self.results.append(addrStr)
                self.results.append(']]')

            self.addrBuffer.clear()
            self.descBuffer.clear()
            self.state = self.BODY
        else:
            self.handle_data(c)

    def handle_data(self, c):
        if self.state == self.DESC:
            self.descBuffer.append(c)
            return

        if self.state == self.ADDRESS:
            self.addrBuffer.append(c)
            return

        if self.state == self.LINK:
            # Expected '(', but got another character:
            # the bracketed text is not a link description, so restore the body text.
            self.results.append('[')
            self.results.extend(self.descBuffer)
            self.results.append(']')
            self.descBuffer.clear()
            self.state = self.BODY
        self.results.append(c)

    def close(self):
        """Append all buffered data to the results."""
        if self.descBuffer:
            self.results.append('[')
            self.results.extend(self.descBuffer)
            self.descBuffer.clear()
        if self.addrBuffer:
            self.results.append('](')
            self.results.extend(self.addrBuffer)
            self.addrBuffer.clear()
        # incomplete Markdown links are adopted unchanged


def reformat_links():
    """Change Markdown links to wikilinks.
    
    Note: this is experimental and disabled by default.
    """
    # Loop through all files with the ".md" extension, including subdirectories.

    linkParser = MdLinkParser()
    for noteFile in glob.iglob('**/*.md', recursive=True):
        print(f'Reformatting links in "{noteFile}" ...')
        with open(noteFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        newlines = []
        for line in lines:
            if '](' in line:
                # line may contain a Markdown link
                line = linkParser.to_wikilinks(line)
            newlines.append(line)
        with open(noteFile, 'w', encoding='utf-8') as f:
            f.writelines(newlines)


def main(backticks=False, wikilinks=False, preserveAt=False):
    """Run the converter
    
    Optional arguments:
        backticks: bool -- If True, verbatim blocks and inline code are marked with backticks.
    """
    print(f'*** Convert Zim export in "{os.getcwd()}" to Obsidian ***\n')
    if RENAME_PAGES:
        rename_pages()
    if REMOVE_FIRST_LINE:
        remove_first_line()
    if CHANGE_MARKDOWN_STYLE:
        change_md_style(backticks, preserveAt)
    if wikilinks:
        reformat_links()
    print('\nDone.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Post-process Zim Markdown export for use with Obsidian',
        epilog=''
        )
    parser.add_argument(
        '-b', '--backticks',
        action="store_true",
        help='verbatim blocks and inline code are marked with backticks'
        )
    parser.add_argument(
        '-w', '--wikilinks',
        action="store_true",
        help='Convert Markdown links to wikilinks'
        )
    parser.add_argument(
        '-@', '--preserve_at',
        action="store_true",
        help='Do not convert Zim tags to Obsidian tags'
        )
    args = parser.parse_args()
    main(args.backticks, args.wikilinks, args.preserve_at)

# markdown2md

Rename Markdown files exported by Zim v0.69 for use with e.g. Obsidian.

- Loops through all subdirectories of a *Zim* notebook Markdown export.
- Replaces the ".markdown" extension with ".md". 
- Fixes internal links to other notes.

# zim2obsidian

Convert Zim export to Obsidian.

- Loops through all subdirectories of a *Zim* notebook Markdown export.
- Removes each noteFile's first level heading and renames the file accordingly. 
- Converts internal links to other pages from Markdown standard to Obsidian style.

Usage:

1. Export a *Zim* Notebook to Markdown (Export each page to a separate file).
2. Make sure the Markdown files have the ".md" extension. If not, run *markdown2md.py* first.
3. Copy this Python script into the export root directory. 
4. Start it by double clicking on it or from the console. 

## Requirements

- A Python installation (version 3.6 or newer).

## Download

### .markdown to .md converter

Save the file [markdown2md.py](https://raw.githubusercontent.com/peter88213/markdown2md/main/src/markdown2md.py).

### Zim to Obsidian converter

Save the file [markdown2md.py](https://raw.githubusercontent.com/peter88213/markdown2md/main/src/zim2obsidian.py).

## Usage

1. Have *Zim* export the notebook to Markdown (export each page to a separate file). 
2. Copy the Python script **markdown2md.py** into the export root directory. 
3. Start it by double clicking on it or from the console. 


## License

Published under the MIT License (https://opensource.org/licenses/mit-license.php)

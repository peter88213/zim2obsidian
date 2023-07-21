# zim2obsidian

Convert Zim Markdown export to Obsidian.

- Loops through all subdirectories of a *Zim* notebook Markdown export.
- Removes each note's first level heading and renames the file accordingly. 
- Replaces Setext-style headers with Atx-style headers.
- Converts horizontal rulers.
- Converts internal links to other pages from Markdown standard to Obsidian style.

Note: The Zim Markdown export is specified [here](https://github.com/zim-desktop-wiki/zim-desktop-wiki/blob/develop/zim/formats/markdown.py) and [here](https://github.com/zim-desktop-wiki/zim-desktop-wiki/blob/develop/zim/formats/plain.py).

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [zim2obsidian.py](https://raw.githubusercontent.com/peter88213/markdown2md/main/src/zim2obsidian.py).

## Usage

1. Have *Zim* export the notebook to Markdown (export each page to a separate file). 
2. Make sure the Markdown files have the ".md" extension. If not, run **markdown2md.py** first.
3. Copy this Python script **zim2obsidian** into the export root directory. 
4. Start it by double clicking on it or from the console. 

---

## Feature requests?

Be aware, this is open source software, and you can implement your own features either locally
after downloading and unpacking the [latest release](https://github.com/peter88213/zim2obsidian/releases/latest), 
or in your own fork.

You also can go to the ["discussions" forum](https://github.com/peter88213/zim2obsidian/discussions) 
to discuss your idea.

---------

# markdown2md

Rename Markdown files exported by Zim v0.69 for use with e.g. Obsidian.

- Loops through all subdirectories of a *Zim* notebook Markdown export.
- Replaces the ".markdown" extension with ".md". 
- Fixes internal links to other notes.

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [markdown2md.py](https://raw.githubusercontent.com/peter88213/markdown2md/main/src/markdown2md.py).

## Usage

1. Have *Zim* export the notebook to Markdown (export each page to a separate file). 
2. Copy the Python script **markdown2md.py** into the export root directory. 
3. Start it by double clicking on it or from the console. 

------------

## License

Published under the [MIT License](https://opensource.org/licenses/mit-license.php)

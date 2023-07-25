# zim2obsidian

Post-process Zim Markdown export for use with Obsidian.

## Features

Loops through all subdirectories of a *Zim* notebook Markdown export.

- Renames pages according to the names given by the top first level heading.
- Removes each note's first line. 
- Converts links from standard Markdown style to Obsidian style (one link per line).
- Converts several Markdown formattings to Obsidian style:
    - Replaces Setext-style headers with Atx-style headers.
    - Converts horizontal rulers.
    - Converts highlighting.
    - Converts checkboxes.
    - Converts tags.

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [zim2obsidian.py](https://raw.githubusercontent.com/peter88213/markdown2md/main/src/zim2obsidian.py).

## Usage

1. Have *Zim* export the notebook to Markdown (export each page to a separate file). 
2. Make sure the Markdown files have the ".md" extension. If not, run [markdown2md.py](https://gist.github.com/peter88213/1fefac8f970a89b05bb20befbd8433da) first.
3. Copy this Python script **zim2obsidian** into the export root directory. 
4. Start it by double clicking on it or from the console. 

---

## Feedback? Ideas? Feature requests?

Be aware, this is open source software, and you can implement your own features either locally
after downloading and unpacking the [latest release](https://github.com/peter88213/zim2obsidian/releases/latest), 
or in your own fork.

You also can go to the ["discussions" forum](https://github.com/peter88213/zim2obsidian/discussions) 
to discuss your idea.


------------

## License

Published under the [MIT License](https://opensource.org/licenses/mit-license.php)

# zim2obsidian

Post-process Zim Markdown export for use with Obsidian.


## Features

Loops through all subdirectories of a *Zim* notebook Markdown export.

- Renames pages according to the names given by the top first level heading.
- Removes each note's first line. 
- Converts Markdown links to wikilinks (optional).
- Converts several Markdown formattings to Obsidian style:
    - Replaces Setext-style headers with Atx-style headers.
    - Converts horizontal rulers.
    - Converts highlighting.
    - Converts checkboxes.
    - Converts tags.
    - Converts verbatim blocks to "fenced" code blocks.
    

## Requirements

- A Python installation (version 3.6 or newer).


## Download

Save the file [zim2obsidian.py](https://raw.githubusercontent.com/peter88213/zim2obsidian/main/src/zim2obsidian.py).


## Suggested workflow

1. If you use indentiation in your *Zim* notebook, consider running the **subst_indent.py** tool first. 
2. Have *Zim* export the notebook to Markdown (export each page to a separate file). 
3. Make sure the Markdown files have the ".md" extension. If not, run the **markdown2md.py** tool first.
4. If you have substituted indentiation with the **subst_indent.py** preprocessor, run the **indent_md.py** tool now.
5. Copy **zim2obsidian.py** into the export root directory. 
6. Start it by double clicking on it or from the console. 


## Usage of the zim2obsidian.py script

```
zim2obsidian.py [-h] [-b]

options:
  -h, --help   show a help message and exit
  -b, --backticks  verbatim blocks and inline code are marked with backticks
```

### The "backticks" option explained

*Zim* exports "verbatim" blocks indented with tabs.
By default, *zim2obsidian.py* encloses such blocks with three backticks, 
so that *Obsidian* recognizes them as code blocks.
Inline code markup is not supported by regular *Zim*.

However, you can enclose inline code with backticks in *Zim*, and
"fence" code blocks with three backticks, as usual in GitHub flavored markdown. 
Then you can call *zim2obsidian.py* with the `--backticks` argument. 
The script then keeps the backticks-enclosed passages verbatim. 
Leading tabs are passed through without adding code block markers.
 
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

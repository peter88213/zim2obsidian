"""Test script for the zim2obsidian script

Requires Python 3.9+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import os
import glob
from shutil import copyfile
import zim2obsidian

TEST_DIR = '../test/workdir'
TEST_INPUT = 'Junk.md'
TEST_OUTPUT = 'Home.md'
SUBPAGE1 = 'subpage.md'
SUBPAGE2 = 'C++.md'
ORIGINAL_FILE = '../data/original.md'
REFERENCE_FILE = '../data/processed.md'
WIKILINKS_FILE = '../data/wikilinks.md'
BACKTICKS_FILE = '../data/backticks.md'

os.makedirs(TEST_DIR, exist_ok=True)
os.chdir(TEST_DIR)


def read_file(inputFile):
    """Read a utf-8 encoded text file and return the contents as a string."""
    with open(inputFile, 'r', encoding='utf-8') as f:
        return f.read()


class SinglePageTest(unittest.TestCase):
    """Test case: convert a single page exported by zim."""

    def setUp(self):
        copyfile(ORIGINAL_FILE, TEST_INPUT)
        copyfile(f'../data/{SUBPAGE1}', f'../workdir/{SUBPAGE1}')
        copyfile(f'../data/{SUBPAGE2}', f'../workdir/{SUBPAGE2}')

    def test_zim2obsidian(self):
        zim2obsidian.main()
        self.assertEqual(read_file(TEST_OUTPUT), read_file(REFERENCE_FILE))

    def tearDown(self):
        for testFile in glob.iglob('**/*.md', recursive=True):
            os.remove(testFile)


class BackticksTest(unittest.TestCase):
    """Test case: convert a single page exported by zim with backticks as code markers."""

    def setUp(self):
        copyfile(ORIGINAL_FILE, TEST_INPUT)
        copyfile(f'../data/{SUBPAGE1}', f'../workdir/{SUBPAGE1}')
        copyfile(f'../data/{SUBPAGE2}', f'../workdir/{SUBPAGE2}')

    def test_zim2obsidian(self):
        zim2obsidian.main(backticks=True)
        self.assertEqual(read_file(TEST_OUTPUT), read_file(BACKTICKS_FILE))

    def tearDown(self):
        for testFile in glob.iglob('**/*.md', recursive=True):
            os.remove(testFile)


class WikiLinksTest(unittest.TestCase):
    """Test case: convert a single page exported by zim."""

    def setUp(self):
        copyfile(ORIGINAL_FILE, TEST_INPUT)
        copyfile(f'../data/{SUBPAGE1}', f'../workdir/{SUBPAGE1}')
        copyfile(f'../data/{SUBPAGE2}', f'../workdir/{SUBPAGE2}')

    def test_zim2obsidian(self):
        zim2obsidian.REFORMAT_LINKS = True
        zim2obsidian.main()
        self.assertEqual(read_file(TEST_OUTPUT), read_file(WIKILINKS_FILE))

    def tearDown(self):
        for testFile in glob.iglob('**/*.md', recursive=True):
            os.remove(testFile)


if __name__ == "__main__":
    unittest.main()

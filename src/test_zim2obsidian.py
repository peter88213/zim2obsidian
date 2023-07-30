"""Test script for the zim2obsidian script

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/zim2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import os
from shutil import copyfile
import zim2obsidian

TEST_DIR = '../test/workdir'
TEST_INPUT = 'Junk.md'
TEST_OUTPUT = 'Home.md'
ORIGINAL_FILE = '../data/original.md'
REFERENCE_FILE = '../data/processed.md'
WIKILINKS_FILE = '../data/wikilinks.md'

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

    def test_zim2obsidian(self):
        zim2obsidian.main()
        self.assertEqual(read_file(TEST_OUTPUT), read_file(REFERENCE_FILE))

    def tearDown(self):
        os.remove(TEST_OUTPUT)


class WiliLinksTest(unittest.TestCase):
    """Test case: convert a single page exported by zim."""

    def setUp(self):
        copyfile(ORIGINAL_FILE, TEST_INPUT)

    def test_zim2obsidian(self):
        zim2obsidian.REFORMAT_LINKS = True
        zim2obsidian.main()
        self.assertEqual(read_file(TEST_OUTPUT), read_file(WIKILINKS_FILE))

    def tearDown(self):
        os.remove(TEST_OUTPUT)


if __name__ == "__main__":
    unittest.main()

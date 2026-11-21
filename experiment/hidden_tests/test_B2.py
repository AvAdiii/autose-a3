"""Hidden acceptance tests for B2 (empty attribute list)."""
import unittest
import markdown


def md(src):
    return markdown.markdown(src, extensions=["attr_list"])


class HiddenB2(unittest.TestCase):
    def test_empty_list_on_header(self):
        self.assertEqual(md("# Title {: }"), "<h1>Title</h1>")

    def test_empty_list_without_space_on_block(self):
        self.assertEqual(md("Some paragraph\n{:}"), "<p>Some paragraph</p>")

    def test_empty_list_inline(self):
        self.assertEqual(md("*hi*{: }"), "<p><em>hi</em></p>")

    def test_non_empty_lists_unchanged(self):
        self.assertEqual(md("# Title {: .a #b }"), '<h1 class="a" id="b">Title</h1>')

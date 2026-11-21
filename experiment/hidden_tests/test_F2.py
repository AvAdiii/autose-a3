"""Hidden acceptance tests for F2 (exclude headings from the TOC)."""
import unittest
import markdown

SRC = "# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n\n## Usage\n"


def names(tokens):
    out = []
    for t in tokens:
        out.append(t["name"])
        out += names(t["children"])
    return out


class HiddenF2(unittest.TestCase):
    def setUp(self):
        self.md = markdown.Markdown(extensions=["toc", "attr_list"])
        self.html = self.md.convert(SRC)

    def test_excluded_heading_not_in_toc(self):
        self.assertNotIn('href="#contents"', self.md.toc)
        self.assertIn('href="#install"', self.md.toc)
        self.assertIn('href="#usage"', self.md.toc)
        self.assertIn('href="#guide"', self.md.toc)

    def test_excluded_heading_keeps_its_id(self):
        self.assertRegex(self.html, r'<h2[^>]*id="contents"[^>]*>Contents</h2>')

    def test_toc_tokens_exclude_heading(self):
        self.assertEqual(names(self.md.toc_tokens), ["Guide", "Install", "Usage"])

    def test_headings_without_class_unchanged(self):
        m = markdown.Markdown(extensions=["toc", "attr_list"])
        m.convert("# A\n\n## B {: .other }\n")
        self.assertEqual(names(m.toc_tokens), ["A", "B"])

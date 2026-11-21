"""Hidden acceptance tests for F1 (wikilinks display label)."""
import unittest
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension


class HiddenF1(unittest.TestCase):
    def test_label_is_shown_and_target_is_linked(self):
        html = markdown.markdown("[[Getting Started|read the guide]]", extensions=["wikilinks"])
        self.assertEqual(html, '<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>')

    def test_whitespace_around_pipe_ignored(self):
        html = markdown.markdown("[[Getting Started | read the guide]]", extensions=["wikilinks"])
        self.assertEqual(html, '<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>')

    def test_config_applies_to_labelled_links(self):
        ext = WikiLinkExtension(base_url="/wiki/", end_url=".html", html_class="w")
        html = markdown.markdown("[[Page|Label]]", extensions=[ext])
        self.assertEqual(html, '<p><a class="w" href="/wiki/Page.html">Label</a></p>')

    def test_plain_wikilink_unchanged(self):
        html = markdown.markdown("[[Getting Started]]", extensions=["wikilinks"])
        self.assertEqual(html, '<p><a class="wikilink" href="/Getting_Started/">Getting Started</a></p>')

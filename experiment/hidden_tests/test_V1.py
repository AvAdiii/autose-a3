"""Hidden acceptance tests for V1 (external links), per the maintainer's clarification on the issue."""
import unittest
import xml.etree.ElementTree as ET
import markdown


def links(src, **kw):
    html = markdown.markdown(src, **kw)
    root = ET.fromstring("<div>" + html + "</div>")
    return [a.attrib for a in root.iter("a")]


class HiddenV1(unittest.TestCase):
    def test_external_link_gets_target_and_rel(self):
        (a,) = links("[docs](https://example.com/x)", extensions=["external_links"])
        self.assertEqual(a.get("target"), "_blank")
        self.assertEqual(set(a.get("rel", "").split()), {"noopener", "noreferrer"})
        self.assertEqual(a.get("href"), "https://example.com/x")

    def test_internal_links_untouched(self):
        for src in ("[a](/docs/)", "[a](#x)", "[a](mailto:me@example.com)", "[a](page.html)"):
            with self.subTest(src=src):
                (a,) = links(src, extensions=["external_links"])
                self.assertNotIn("target", a)
                self.assertNotIn("rel", a)

    def test_autolink_and_http_external(self):
        (a,) = links("<https://example.com>", extensions=["external_links"])
        self.assertEqual(a.get("target"), "_blank")
        (b,) = links("[a](http://example.com)", extensions=["external_links"])
        self.assertEqual(b.get("target"), "_blank")

    def test_off_by_default(self):
        (a,) = links("[docs](https://example.com/x)")
        self.assertNotIn("target", a)

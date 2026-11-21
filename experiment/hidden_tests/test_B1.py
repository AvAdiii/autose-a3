"""Hidden acceptance tests for B1 (fenced_code + attr_list boolean options). Never shown to any agent."""
import unittest
import markdown

EXT = ["fenced_code", "attr_list"]


class HiddenB1(unittest.TestCase):
    def test_bare_linenums_does_not_crash_and_renders_code(self):
        html = markdown.markdown("``` { .python linenums }\nprint(1)\n```", extensions=EXT)
        self.assertIn('<code class="language-python"', html)
        self.assertIn("print(1)", html)

    def test_explicit_boolean_options_do_not_crash(self):
        for attrs in ('linenums="true"', 'linenums="1"', "guess_lang", "noclasses", 'use_pygments="false"'):
            with self.subTest(attrs=attrs):
                html = markdown.markdown("``` { .python %s }\nx = 1\n```" % attrs, extensions=EXT)
                self.assertIn("x = 1", html)
                self.assertIn("<pre", html)

    def test_other_attributes_still_rendered(self):
        html = markdown.markdown('``` { .python data-x="1" linenums }\ny\n```', extensions=EXT)
        self.assertIn('data-x="1"', html)

    def test_with_codehilite_still_works(self):
        html = markdown.markdown("``` { .python linenums }\nprint(1)\n```", extensions=EXT + ["codehilite"])
        self.assertIn("print", html)

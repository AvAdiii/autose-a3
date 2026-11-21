## Specification
- **FR-001** When `fenced_code` and `attr_list` are enabled without `codehilite`, a fenced block with a boolean option (`linenums`, `guess_lang`, `noclasses`, `use_pygments`) shall render as a code block without raising.
- **FR-002** Other attributes on such a block shall still be rendered.

## Design
`FencedBlockPreprocessor.run` writes every attr_list key/value onto `<code>` when Pygments is not used. Boolean options are parsed to `True`/`False`/`None` by `handle_attrs`, which `_escape_attrib_html` cannot serialize. Only string values are written now; the Pygments-only options are dropped, which matches what codehilite does when it is disabled.

## Test report
3 new tests pass. Full suite: 1117 passed, 52 skipped. flake8 clean. Changelog entry added.

<!-- The maintainer answer posted on the issue after the first run stopped with questions. Written before any run. -->
Thanks for the questions. Decisions:

1. Add a new built-in extension called `external_links`, loaded with `extensions=['external_links']`. Nothing changes unless it is enabled.
2. A link is external when its `href` starts with `http://` or `https://`. Relative links, `#anchors` and `mailto:` links are not external.
3. Every external `<a>` element gets `target="_blank"` and `rel="noopener noreferrer"`. This includes automatic links like `<https://example.com>`.
4. Images are not affected. No configuration options for now.

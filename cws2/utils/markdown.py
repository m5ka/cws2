from markupsafe import Markup
from mistune import create_markdown

_markdown = create_markdown(plugins=["strikethrough", "superscript", "subscript", "spoiler"])


def parse_markdown(markdown):
    return Markup(_markdown(markdown))

import os
from typing import Union

from jinja2 import Environment, FileSystemLoader

from app.log.console import log_info

env = Environment(
    loader=FileSystemLoader(f"assets/templates")
)


def render_template(
    name: str, context: dict[str, Union[str, int]] | None = None
):
    """
    Renders a template with the given name and context.

    Args:
        name (str): The name of the template file.
        context (dict): The context to render the template with.

    Returns:
        str: The rendered template as a string.
    """
    template = env.get_template(f"{name}.html")
    log_info(template.filename)
    return template.render(context)

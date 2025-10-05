import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.project_slug }}"
description = "{{ cookiecutter.project_short_description }}"

if not re.match(MODULE_REGEX, module_name):
    print(
        f"ERROR: The project slug ({module_name}) is not a valid Python module name.\n"
        "Please do not use a - and use _ instead"
    )
    # Exit to cancel project
    sys.exit(1)

if len(description) > 80:
    print(
        f"ERROR: The short description was more than 80 characters ({len(description)}).\n"
        "Please try a shorter description."
    )
    # Exit to cancel project
    sys.exit(1)

if "\n" in description:
    print(
        "ERROR: The short description had a line break.\n"
        "Please remove all line breaks from the description."
    )
    # Exit to cancel project
    sys.exit(1)

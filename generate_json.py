import json
import re

from typing import Iterator

from pathlib import Path


template = re.compile(r"{{cookiecutter\.([\w\d_]+)}}")

TEMPLATE_ROOT_NAME = "{{cookiecutter.project_slug_name}}"


def get_all_tags() -> Iterator[str]:
    template_root = Path(TEMPLATE_ROOT_NAME)

    for curr_path in template_root.rglob("*"):
        yield from template.findall(curr_path.as_posix())

        if not curr_path.is_file():
            continue

        with curr_path.open("r") as curr_file:
            full_file = curr_file.read()
            yield from template.findall(full_file)


if __name__ == "__main__":
    with Path("cookiecutter.json").open("r+") as cookiecutter_json:
        cookie_json = json.load(cookiecutter_json)
        cookiecutter_json.seek(0)

        for curr_tag in get_all_tags():
            if curr_tag not in cookie_json:
                cookie_json[curr_tag] = ""

        json.dump(cookie_json, cookiecutter_json, sort_keys=True, indent=2)
        cookiecutter_json.write("\n")

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_prompt(path):

    prompt_path = BASE_DIR / path

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

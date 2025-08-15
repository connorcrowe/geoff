from pathlib import Path
from jinja2 import Template

PROMPT_DIR = Path(__file__).resolve().parent 

def load_prompt_template(name: str) -> Template:
    path = PROMPT_DIR / f"{name}.md"
    with open(path, "r", encoding="utf-8") as f:
        return Template(f.read())

SYSTEM_PROMPT = load_prompt_template("system_prompt.sql")
CORRECTIVE_PROMPT = load_prompt_template("corrective_prompt.sql")
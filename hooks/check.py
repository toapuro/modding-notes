import logging, re
from packaging.version import Version

log = logging.getLogger('mkdocs')

ANNOTATIONS = [
    "TODO",
    "FIXME",
    "NOTE"
]

def on_page_markdown(markdown, page, **kwargs):
    path = page.file.src_uri
    
    for annotation in ANNOTATIONS:
        for m in re.finditer(f'<!-- ({annotation}): ?(.*) -->', markdown):
            text = f"Doc file '{path}' contains {annotation}: {m[2]}"

            if(annotation == "NOTE"):
                log.info(text)
                print(f"::notice title=mkdocs::{text}")
                continue

            log.warning(text)
            print(f"::warning title=mkdocs::{text}")
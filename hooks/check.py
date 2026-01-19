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
        for m in re.finditer(f'({annotation}): ?(.*)', markdown):
            log.warning(f"Doc file '{path}' contains {annotation}: {m[0]}")
            
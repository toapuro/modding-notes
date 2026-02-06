from pathlib import Path

src_dir = Path("./docs/content")
out_file = Path("./docs/all.txt")

def gather_md(*args, **kwargs):
    md_files = sorted(src_dir.rglob("*.md"))

    with out_file.open("w", encoding="utf-8") as out:
        for md in md_files:
            out.write(f"\n\n# [{md.relative_to(src_dir)}]\n\n")
            out.write(md.read_text(encoding="utf-8"))
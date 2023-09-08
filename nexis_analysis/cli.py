# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Analyse documents retrieved from Nexis Uni"""
import click
from collections import defaultdict
import csv
import hashlib
import pathlib
import shutil
import subprocess

@click.command("convert")
@click.option("-i", "--input-dir", type=click.Path(
    exists=True, dir_okay=True, path_type=pathlib.Path), required=True)
@click.option("-o", "--output-dir", type=click.Path(
    dir_okay=True, path_type=pathlib.Path), required=True)
def convert_docx_to_gfm(input_dir: pathlib.Path, output_dir: pathlib.Path):
    """Convert .docx files in a directory to GitHub-flavoured Markdown"""
    pandoc_cmd = shutil.which("pandoc")
    if pandoc_cmd is None:
        raise Exception("pandoc could not be found")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    results = []
    file_hashes = defaultdict(list)
    summary_path = output_dir / "summary.csv"
    summary_field_names = ["name_hash", "source_file_name", "source_file_sha256", "target_file_name", "conversion_rc"]
    with summary_path.open(mode="w", encoding="utf-8", newline="") as summary_file:
        writer = csv.DictWriter(summary_file, summary_field_names)
        writer.writeheader()
        for item in input_dir.glob("**/*.docx"):
            file_hash = hashlib.sha256(item.read_bytes()).hexdigest()
            name_hash = hashlib.shake_128(str(item).encode("utf-8")).hexdigest(20)
            conversion_result = subprocess.run([
                pandoc_cmd,
                "--wrap=preserve",
                "-t",
                "gfm",
                "-o",
                f"{output_dir / name_hash}.md",
                item,
            ])
            writer.writerow({
                "name_hash": name_hash,
                "source_file_name": str(item),
                "source_file_sha256": file_hash,
                "target_file_name": f"{name_hash}.md"
                "conversion_rc": conversion_result.returncode,
            })
            file_hashes[file_hash].append(str(item))
    for fh in file_hashes:
        if len(file_hashes[fh]) > 1:
            print("Duplicate file contents:")
            for name in file_hashes[fh]:
                print("   -", name)
    print(f"Converted {len(file_hashes)} files")



if __name__ == "__main__":
    convert_docx_to_gfm(None, None)

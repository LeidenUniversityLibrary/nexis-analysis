# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Analyse documents retrieved from Nexis Uni"""
import click
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
    for item in input_dir.glob("**/*.docx"):
        # print(item)
        file_hash = hashlib.shake_128(item.read_bytes()).hexdigest(40)
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
        print(name_hash, conversion_result.returncode)



if __name__ == "__main__":
    convert_docx_to_gfm(None, None)

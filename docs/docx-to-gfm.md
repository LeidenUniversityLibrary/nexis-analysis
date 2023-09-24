---
title: Convert docx to GitHub-flavoured Markdown
# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: CC-BY-4.0
---

# Install Pandoc

Follow the [Pandoc installation instructions](https://pandoc.org/installing.html)
to install Pandoc.

# Run conversion

Our script accepts a directory of input files, a directory to store the output
files and calls Pandoc for each input file.

The input files may be located in subdirectories.
The output files will all be in a single directory.
To make sure that filenames do not collide in the output directory,
their names are hashes of the input filenames.

!!! note
    The conversion script does not exclude overview files.

Run with [Hatch]:

```sh
hatch run nexis convert -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

If you installed the package, you can run:

```sh
nexis convert -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

[Hatch]: https://hatch.pypa.io/latest/

!!! note
    The package has not yet been published in PyPI, so the way to install it is
    by building it locally and installing the resulting package.

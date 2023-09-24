---
title: Installation
# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: CC-BY-4.0
---

The scripts are written in Python and require Python 3.9 or newer to run.

The scripts have not been published to PyPI, so to install them you can either
install the package from the git repository using pip, or run the scripts with
Hatch.
We describe how to use Hatch below.

# Install Hatch

Follow the [Hatch installation instructions][Hatch] to install Hatch.

[Hatch]: https://hatch.pypa.io/latest/install/

# Clone the git repository

```sh
git clone https://github.com/LeidenUniversityLibrary/nexis-analysis.git
cd nexis-analysis
```

# Run a `nexis` command

After the previous steps, you should be in the `nexis-analysis` directory.
To check that the tool works, run:

```sh
hatch run nexis --help
```

This should show the available commands:

```output
Usage: nexis [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  analyse  Extract information from GFM documents in a directory
  convert  Convert .docx files in a directory to GitHub-flavoured Markdown
  terms    Extract marked-up search terms or phrases from GFM documents...
```

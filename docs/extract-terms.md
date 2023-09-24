---
title: Extract search terms from converted files
# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: CC-BY-4.0
---

Nexis Uni marks the phrases or terms that caused the article to match in the
files.
This allows us to find which terms are in which article by their markup.

The result of the command is a CSV file linking filenames and counts of terms.

# Usage

The input directory must contain the Markdown files.
The output directory (defaults to the input directory if not specified) will
have a file named *terms-results.csv*.

Run with Hatch:

```sh
hatch run nexis terms -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

If you installed the package, you can run:

```sh
nexis terms -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

!!! note
    Marked phrases and terms are only extracted from the body of the articles.

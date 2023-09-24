---
title: Extract metadata from converted files
# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
# SPDX-License-Identifier: CC-BY-4.0
---

Nexis Uni includes fairly standardised metadata for each article, such as the
title, name of the publication, publication date, a byline and the number of
words in the article body.
This command creates a CSV file that includes these metadata for each input
file.

# Usage

The input directory must contain the Markdown files.
The output directory (defaults to the input directory if not specified) will
have a file named *analysis-results.csv*.

Run with Hatch:

```sh
hatch run nexis analyse -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

If you installed the package, you can run:

```sh
nexis analyse -i INPUT_DIRECTORY -o OUTPUT_DIRECTORY
```

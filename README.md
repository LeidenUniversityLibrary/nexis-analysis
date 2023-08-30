# Parsing Nexis Uni newspapers documents

## Existing tools

The R package [LexisNexisTools] appears to be maintained and appropriate for
what we intend to do.

However, it expects every article to start with a specific phrase and
when each article is a separate Word .docx file, there is no common phrase.

We have earlier experience with [python-docx], which appears to no longer be
supported.
There are almost 1000 forks. It is difficult to understand which is the most
compatible with the documents in our corpus.

At least two GitHub repositories with a license appear to support (part of) our
research, although their documentation is minimal and the code looks brittle.
These repos are [seolub/Nexis_uni_parser] and [zhong3401/nexis_uni_extractor].

[LexisNexisTools]: https://github.com/JBGruber/LexisNexisTools
[python-docx]: https://github.com/python-openxml/python-docx
[seolub/Nexis_uni_parser]: https://github.com/seolub/Nexis_uni_parser
[zhong3401/nexis_uni_extractor]: https://github.com/zhong3401/nexis_uni_extractor

Other tools can read and convert docx files too, like [pandoc].
Pandoc does not extract any images, but if we are just looking for text data,
that is fine.

[pandoc]: https://pandoc.org

## Combining tools

Use Pandoc to convert docx to Markdown.
Then use regular expressions to find metadata in the file.
Glue sentences back into paragraphs.

## Methods

- extract body of documents
- count the number of terms for each document
- metadata extraction
- create a table of metadata and counts
- topic modelling to find clusters of documents?
- regex

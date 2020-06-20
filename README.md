# hetzner-fix-report

Fixes Hetzner CSV reports by cleaning the CSV and merging project name from PDF.

## Installation

This project is hosted on [PyPI](https://pypi.org/project/hetzner-fix-report/) and can therefore be installed easily through pip:

```
pip install hetzner_fix_report
```

Dependending on your setup you may need to add `--user` after the install.

## Usage

Use the command line interface to combine a `csv` and `pdf` file:

```
hetzner-fix-report Hetzner_2020-01-05_RXXXXXXXXXX.csv Hetzner_2020-01-05_RXXXXXXXXXX.pdf
```

Or shorten it using brace expansion:

```
hetzner-fix-report Hetzner_2020-01-05_RXXXXXXXXXX.{csv,pdf}
```

If you want to save the enriched csv output, use either the `-o` parameter as explained in the program's help or redirect output to a file using `>`.

<# hetzner-fix-report

Takes invoice CSV files from Hetzner and changes the formatting, splitting columns which contain various information into multiple columns.

Versions <1.0 took the Hetzner CSV *and* PDF as input, and extracted e.g. project information from the PDF.
However, today this information is also included in the CSV, so the PDF is no longer needed.
If you have older invoices, you can re-download them from the Hetzner invoice page in the new format.
Otherwise, if you can't re-download the invoice, you can use the old version of hetzner-fix-report.

Fixes Hetzner CSV reports by cleaning the CSV and merging project name from PDF.


## Installation

This project is hosted on [PyPI](https://pypi.org/project/hetzner-fix-report/) and can therefore be installed easily through pip:

```
pip install hetzner_fix_report
```

Depending on your setup you may need to add `--user` after the installation.

## Usage
### Single report
Use the command line interface to process a `csv` file:

```
hetzner-fix-report Hetzner_2020-01-05_RXXXXXXXXXX.csv
```

If you want to save the enriched csv output, use either the `-o` parameter as explained in the program's help or redirect output to a file using `>`.

### Batchwise processing
When in a directory that holds multiple `csv` and `pdf` files the following shell script should call the tool and save its output within a newly created subdirectory:

```
mkdir -p fix
for csv in *.csv; do hetzner-fix-report -o "fix/$csv" "$csv"; done
```

## Original & enriched format
Hetzner's original CSV reports have the problem of being unprecise and not machine readable.
This is especially noticeable in the long multiline comment column that is mostly human readable.
The enriched format has the following keys and exemplary values:

Key | Example | New
:-|:-:| :-:
`id` | `2520725` | ✔
`name` | `my-server` | ✔
`project` | `My Project` | ✔
`type` | `cx31` |
`quantity` | `1` |
`usage_hours` | `42` | ✔
`price` | `8.9` |
`price_netto` | `4.9` |
`price_max` | `2.49` | ✔
`day_from` | `2020-06-01` |
`day_to` | `2020-06-30` |
`is_backup` | `False` | ✔
`is_server` | `True` | ✔
`is_ceph` | `False` | ✔

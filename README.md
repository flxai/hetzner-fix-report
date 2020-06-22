# hetzner-fix-report
Fixes Hetzner CSV reports by cleaning the CSV and merging project name from PDF.

## Installation
### Preliminary libraries

Debian, Ubuntu, etc

```
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
```

Fedora, Red Hat, etc

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python-devel redhat-rpm-config
```

Arch, etc

```
sudo pacman -S poppler
```

### Python package
This project is hosted on [PyPI](https://pypi.org/project/hetzner-fix-report/) and can therefore be installed easily through pip:

```
pip install hetzner_fix_report
```

Dependending on your setup you may need to add `--user` after the install.

## Usage
### Single report
Use the command line interface to combine a `csv` and `pdf` file:

```
hetzner-fix-report Hetzner_2020-01-05_RXXXXXXXXXX.csv Hetzner_2020-01-05_RXXXXXXXXXX.pdf
```

Or shorten it using brace expansion:

```
hetzner-fix-report Hetzner_2020-01-05_RXXXXXXXXXX.{csv,pdf}
```

If you want to save the enriched csv output, use either the `-o` parameter as explained in the program's help or redirect output to a file using `>`.

### Batchwise processing
When in a directory that holds multiple `csv` and `pdf` files the following shell script should call the tool and save its output within a newly created subdirectory:

```
mkdir -p fix
for csv in *.csv; do pdf=${csv%%.*}.pdf; hetzner-fix-report -o "fix/$csv" "$csv" "$pdf"; done
```

## Original & enriched format
Hetzner's original CSV reports have the problem of being unprecise and not machine readable.
This is especially noticeable in the long multiline comment column that may is mostly human readable.
Currently the PDF report contains additional information about the entry's (server/backup) associated project.
Since this information is not contained within the CSV reports I wanted to fix this.
The enriched format has the following keys and examplary values:

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

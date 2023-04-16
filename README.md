# ledes-parser
A package for parsing LEDES format files.

## Installation

To install the package, run:

```bash
pip install ledes-parser
```
# Example Usage
```python
from ledes_parser import parse_ledes_file

with open('tests/sample_data.txt', 'r') as f:
    reader = csv.reader(f, delimiter="|")
    invoices = parse_ledes_file(reader, "1998")
    print(invoices)
```

# LEDES File Formats
This package supports the following LEDES file formats:

* 1998
* 1998B
* 1998BI

# Contributing
Fork the repository on GitHub.
Create a new branch with your changes.
Commit your changes and push them to your fork.
Create a pull request against the main branch of the original repository.
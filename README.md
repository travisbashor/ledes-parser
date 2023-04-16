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

with open('path/to/the/ledes_file.txt', 'r') as f:
    invoices = parse_ledes_file(f, "1998")
    print(invoices)
```

# LEDES File Formats
This package supports the following LEDES file formats:

* LEDES98B
* LEDES98BI
* LEDES98BIV2
* LEDES2000
* LEDESXML20
* LEDESXML21

# Contributing
Fork the repository on GitHub.
Create a new branch with your changes.
Commit your changes and push them to your fork.
Create a pull request against the main branch of the original repository.
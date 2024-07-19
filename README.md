# ledes-parser
A package for parsing LEDES format files. 

Note: this is a WIP. DO NOT RELY ON THIS FOR YOUR LEGAL INVOICING.

## Installation

To install the package, run:

```bash
pip install ledes-parser
```
# Example Usage
```python
from ledes_parser.ledes_parser import get_parser

with open('path/to/the/ledes_file.txt', 'r') as f:
    ledes_data = f.read()

parser = get_parser(spec="98B")
result = parser.parse(ledes_data)
print(result.pretty())
```
That produces a tokenized version of the ledes file. You can see an example of using a transformer to compile them into python in the /notebooks directory.

# LEDES File Formats
This package supports parsing the following LEDES file formats:

* LEDES98B
* (TBD) LEDES98BI
* (TBD) LEDES98BIV2
* (TBD) LEDES2000
* (TBD) LEDESXML20
* (TBD) LEDESXML21

# Contributing
Fork the repository on GitHub.
Create a new branch with your changes.
Commit your changes and push them to your fork.
Create a pull request against the main branch of the original repository.

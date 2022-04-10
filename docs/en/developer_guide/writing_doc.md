# Write Documentation

[Sphinx](https://www.sphinx-doc.org/) is used to generate documentation for Hammer.

## Setup Environment

To generate the documents locally, please install the dependencies with

```shell
pip install -r requirements/doc.txt
```

## File Structure

```shell
/doc/
├── en                    # English documentation
│   ├── Makefile          # Sphinx Makefile
│   ├── _build/           # Static web files
│   ├── api_reference/    # Directory of APIs (generated via docstring)
│   ├── conf.py           # Sphinx configuration
│   ├── developer_guide/  # Directory of developer guide
│   ├── faq.md            # Frequently asked questions
│   ├── index.rst         # Home of documentation
│   ├── make.bat          # Sphinx make script
│   └── user_guide/       # Directory of user guide
└── zh-hans               # Zh-Hans documentation
    ├── Makefile          # Sphinx Makefile
    ├── _build/           # Static web files
    ├── api_reference/    # Directory of APIs (generated via docstring)
    ├── conf.py           # Sphinx configuration
    ├── developer_guide/  # Directory of developer guide
    ├── faq.md            # Frequently asked questions
    ├── index.rst         # Home of documentation
    ├── make.bat          # Sphinx make script
    └── user_guide/       # Directory of user guide
```

## Generate Static Files

Run following command in the root directory of documentation source to generate static files:

```shell
make html
```

To remove generated results, you can simply remove `_build` folder.

## (Optional) Configure Continuous Integration (CI)

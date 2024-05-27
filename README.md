# Edi Challenge

For the last year I've been using [Pants](https://pantsbuild.org) as my build tool for Python projects. Even though for this test such a powerful tool isn't really needed, I'm so used to it that I apologise in advance if it causes to much noise to the person evaluating the test.

## Setup Development MacOS

In order to work with the project you will need to install Pants:

```sh
brew install pantsbuild/tap/pants
```

And have a Python 3.12 interpreter installed on your machine.

Once installed, you can:

- Run tests with `pants test ::`
- Package the project with `pants package ::`
- Package the project with `pants package ::`
- Run the packaged application with `./dist/app.python.edi/bin.pex`
- Run the application directly (without packaging) `pants run app/python/edi/main.py -- --help`

**Note on packaging**: The application is packaged as a binary (See [PEX](https://pex.readthedocs.io/en/v2.1.153/whatispex.html)). This is the default behavior of Pants and I'm an advocate of it.

**Note on Python 3.12**: I have chosen to go with this version because the versions suggested by the challenge 3.6/3.7 have reached end of life, and I already have 3.12 installed on my machine.

In case you don't have access to a Python3.12 installation, I'm sending the packaged application for Linux too, which can be run directly inside a Docker image with: `docker run --rm -ti -v ./edi-linux:/bin/edi python:3.12.0 edi --help`

### Troubleshooting

If you have Python 3.12 installed but Pants is not able to find it, create a `.pants.rc` file and add the path where it exists. For example, I'm using [asdf](https://asdf-vm.com) on my machine and I need to tell Pants about it with:

```toml
# .pants.rc
[python-bootstrap]
search_path = [
    "/Users/anler/.asdf/installs/python/3.12.0/bin"
]
```

If you can't/want install Python 3.12 there's a Docker image that can be used as dev environment.

## Challenge Solution

After dedicating some time to understand the EDI 867 02 file format, and given the time restriction, all I could have done is:

- Parse the files with no third-party dependency. There may exist a library that solves this problem but I couldn't find one quickly
- Restrict the challenge to parsing just the heading segments. I know I'm missing very interesting cases such as when a segment has more or less fields depending on the value of another field on that same segment (this is the reason of `fields: Collection[Collection[str]]` type in the `SegmentParser`)
- Parse each defined transaction fully in memory and then writing to the database. I don't know how big a transaction can be, so I'm assuming they aren't. If they where, my parsing solution would have used a streaming approach

To test the challenge perform these steps:

1. Package the app: `pants package ::`
1. Rename the app for easier use: `mv dist/app.python.edi/bin.pex edi`
1. Create the database: `edi create-db sqlite:///edi.db`
1. Import the example file: `edi import sqlite:///edi.db files/non_interval`

# ddiff

A diff tool for structured data, such as json and yaml.

## Description

`ddiff` is a tool to compare keys and values in structured data files, such as json and yaml.
It compares key existence, value, value type and array sequence. It is aimed to filter difference of structured data, rather than texts in the file, to support finding actual changes in the original file and the changed file.

## Requirement

- Python >= 3.8

## Installation

You can install `ddiff` as a Python cli tool.

```sh
$ git clone git@github.com:shibuiwilliam/ddiff.git
$ cd ddiff
$ make install
```

## Usage and examples

Once installed, you can call `ddiff` in your cli.
Specify two files you would like to compare, and add options if needed.

```
$ ddiff --help
Usage: ddiff [OPTIONS] FILES...

Options:
  -s, --steps BOOLEAN             print results in steps
  -i, --indent_size INTEGER       indentation size
  -l, --line_separator TEXT       line separator
  -o, --output_filepath TEXT      output file path
  -f, --output_format [default|json|yaml]
                                  output format
  -d, --debug BOOLEAN             run in debug mode
  --help                          Show this message and exit.
```

You can find [example json files and yaml files](https://github.com/shibuiwilliam/ddiff/tree/main/examples) to compare to see their differences.
Comparison of [examples/original.json](./examples/original.json) and [examples/comparer.json](./examples/comparer.json):

```sh
# example difference in json files
$ python -m ddiff.main ../examples/original.yaml ../examples/comparer.yaml -s True
-------
x
- different values
    ../examples/original.yaml: ['c', 'a', 1]
    ../examples/comparer.yaml: ['c', 'a', 1, 2]
-------
y
- array in different sequence
    ../examples/original.yaml: [3, 2, 1]
    ../examples/comparer.yaml: [1, 2, 3]
-------
z
- different values
    ../examples/original.yaml: [3, 2, 1]
    ../examples/comparer.yaml: [3, 2, '1']
-------
aa
- different types
    ../examples/original.yaml: CommentedSeq
    ../examples/comparer.yaml: int
-------
bb
- different types
    ../examples/original.yaml: int
    ../examples/comparer.yaml: str
-------
cc
- different types
    ../examples/original.yaml: ScalarFloat
    ../examples/comparer.yaml: int
-------
e
- different values
    ../examples/original.yaml: 11
    ../examples/comparer.yaml: 12
-------
c
└─b
- key not in ../examples/original.yaml
    ../examples/original.yaml: null
    ../examples/comparer.yaml: 2
-------
d
└─e
  └─f
- key not in ../examples/comparer.yaml
    ../examples/original.yaml: 0
    ../examples/comparer.yaml: null
-------
d
└─e
  └─e
- key not in ../examples/original.yaml
    ../examples/original.yaml: null
    ../examples/comparer.yaml: 1
-------
d
└─e
  └─d
    └─m
- different values
    ../examples/original.yaml: 0
    ../examples/comparer.yaml: 1
-------
d
└─e
  └─g
    └─h
      └─h
- key not in ../examples/comparer.yaml
    ../examples/original.yaml: 11
    ../examples/comparer.yaml: null
-------
d
└─e
  └─g
    └─h
      └─j
- different values
    ../examples/original.yaml: 12
    ../examples/comparer.yaml: 11
```

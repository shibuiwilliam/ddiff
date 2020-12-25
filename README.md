# ddiff

A diff tool for structured data, such as json and yaml.


## Description

`ddiff` is a tool to compare keys and values in structured data files, such as json and yaml.
It compares key existence, value, value type and array sequence. It is aimed to filter difference of structured data, rather than texts in the file, to support finding actual changes in the original file and the changed file.

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
  -s, --steps BOOLEAN        print results in steps
  -i, --indent_size INTEGER  indentation size
  -l, --line_separator TEXT  line separator
  -d, --debug BOOLEAN        run in debug mode
  --help                     Show this message and exit.
```

You can find [example json files and yaml files](https://github.com/shibuiwilliam/ddiff/tree/main/examples) to compare to see their differences.

```sh
# example difference in json files
$ ddiff examples/original.json examples/comparer.json -s True
-------
x
- different values
    examples/original.json: ['c', 'a', 1]
    examples/comparer.json: ['c', 'a', 1, 2]
-------
y
- array in different sequence
    examples/original.json: [3, 2, 1]
    examples/comparer.json: [1, 2, 3]
-------
z
- different values
    examples/original.json: [3, 2, 1]
    examples/comparer.json: [3, 2, '1']
-------
aa
- different types
    examples/original.json: CommentedSeq
    examples/comparer.json: int
-------
bb
- different types
    examples/original.json: int
    examples/comparer.json: str
-------
e
- different values
    examples/original.json: 11
    examples/comparer.json: 12
-------
c
└─b
- key not in examples/original.json
    examples/original.json: null
    examples/comparer.json: 2
-------
d
└─e
  └─f
- key not in examples/comparer.json
    examples/comparer.json: null
    examples/original.json: 0
-------
d
└─e
  └─e
- key not in examples/original.json
    examples/original.json: null
    examples/comparer.json: 1
-------
d
└─e
  └─d
    └─m
- different values
    examples/original.json: 0
    examples/comparer.json: 1
-------
d
└─e
  └─g
    └─h
      └─h
- key not in examples/comparer.json
    examples/comparer.json: null
    examples/original.json: 11
-------
d
└─e
  └─g
    └─h
      └─j
- different values
    examples/original.json: 12
    examples/comparer.json: 11
```

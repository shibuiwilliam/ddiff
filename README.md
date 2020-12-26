# ddiff

A diff tool for structured data, such as json and yaml.

## Description

`ddiff` is a tool to compare keys and values in structured data files, such as json and yaml.
It compares key existence, value, value type and array sequence. It is aimed to filter difference of structured data, rather than texts in the file, to support finding actual changes in the original file and the changed file.

## Requirement

- Python >= 3.8

## Installation

You can install from [pypi](https://pypi.org/project/ddiff/) package.

```sh
$ pip install ddiff
```

You can also install `ddiff` as a Python cli tool.

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
# example difference in yaml files
$ ddiff examples/original.yaml examples/comparer.yaml -s True
-------
x
- different values
    examples/original.yaml: ['c', 'a', 1]
    examples/comparer.yaml: ['c', 'a', 1, 2]
-------
y
- array in different sequence
    examples/original.yaml: [3, 2, 1]
    examples/comparer.yaml: [1, 2, 3]
-------
z
- different values
    examples/original.yaml: [3, 2, 1]
    examples/comparer.yaml: [3, 2, '1']
-------
aa
- different types
    examples/original.yaml: CommentedSeq
    examples/comparer.yaml: int
-------
bb
- different types
    examples/original.yaml: int
    examples/comparer.yaml: str
-------
cc
- different types
    examples/original.yaml: ScalarFloat
    examples/comparer.yaml: int
-------
e
- different values
    examples/original.yaml: 11
    examples/comparer.yaml: 12
-------
c
└─b
- key not in examples/original.yaml
    examples/original.yaml: null
    examples/comparer.yaml: 2
-------
d
└─e
  └─f
- key not in examples/comparer.yaml
    examples/original.yaml: 0
    examples/comparer.yaml: null
-------
d
└─e
  └─e
- key not in examples/original.yaml
    examples/original.yaml: null
    examples/comparer.yaml: 1
-------
d
└─e
  └─d
    └─m
- different values
    examples/original.yaml: 0
    examples/comparer.yaml: 1
-------
d
└─e
  └─g
    └─h
      └─h
- key not in examples/comparer.yaml
    examples/original.yaml: 11
    examples/comparer.yaml: null
-------
d
└─e
  └─g
    └─h
      └─j
- different values
    examples/original.yaml: 12
    examples/comparer.yaml: 11
```

You can print the differences in json format:

```sh
$ ddiff examples/original.yaml examples/comparer.yaml -s True  -f json
{
    "x": {
        "status": "different values",
        "examples/original.yaml": [
            "c",
            "a",
            1
        ],
        "examples/comparer.yaml": [
            "c",
            "a",
            1,
            2
        ]
    },
    "y": {
        "status": "array in different sequence",
        "examples/original.yaml": [
            3,
            2,
            1
        ],
        "examples/comparer.yaml": [
            1,
            2,
            3
        ]
    },
    "z": {
        "status": "different values",
        "examples/original.yaml": [
            3,
            2,
            1
        ],
        "examples/comparer.yaml": [
            3,
            2,
            "1"
        ]
    },
    "aa": {
        "status": "different types",
        "examples/original.yaml": "CommentedSeq",
        "examples/comparer.yaml": "int"
    },
    "bb": {
        "status": "different types",
        "examples/original.yaml": "int",
        "examples/comparer.yaml": "str"
    },
    "cc": {
        "status": "different types",
        "examples/original.yaml": "ScalarFloat",
        "examples/comparer.yaml": "int"
    },
    "d.e.d.m": {
        "status": "different values",
        "examples/original.yaml": 0,
        "examples/comparer.yaml": 1
    },
    "d.e.f": {
        "status": "key not in examples/comparer.yaml",
        "examples/original.yaml": 0,
        "examples/comparer.yaml": null
    },
    "d.e.g.h.j": {
        "status": "different values",
        "examples/original.yaml": 12,
        "examples/comparer.yaml": 11
    },
    "d.e.g.h.h": {
        "status": "key not in examples/comparer.yaml",
        "examples/original.yaml": 11,
        "examples/comparer.yaml": null
    },
    "e": {
        "status": "different values",
        "examples/original.yaml": 11,
        "examples/comparer.yaml": 12
    },
    "c.b": {
        "status": "key not in examples/original.yaml",
        "examples/comparer.yaml": 2,
        "examples/original.yaml": null
    },
    "d.e.e": {
        "status": "key not in examples/original.yaml",
        "examples/comparer.yaml": 1,
        "examples/original.yaml": null
    }
}
```

Of course in yaml:

```sh
$ ddiff examples/original.yaml examples/comparer.yaml -s True  -f yaml
aa:
  examples/comparer.yaml: int
  examples/original.yaml: CommentedSeq
  status: different types
bb:
  examples/comparer.yaml: str
  examples/original.yaml: int
  status: different types
c.b:
  examples/comparer.yaml: 2
  examples/original.yaml: null
  status: key not in examples/original.yaml
cc:
  examples/comparer.yaml: int
  examples/original.yaml: ScalarFloat
  status: different types
d.e.d.m:
  examples/comparer.yaml: 1
  examples/original.yaml: 0
  status: different values
d.e.e:
  examples/comparer.yaml: 1
  examples/original.yaml: null
  status: key not in examples/original.yaml
d.e.f:
  examples/comparer.yaml: null
  examples/original.yaml: 0
  status: key not in examples/comparer.yaml
d.e.g.h.h:
  examples/comparer.yaml: null
  examples/original.yaml: 11
  status: key not in examples/comparer.yaml
d.e.g.h.j:
  examples/comparer.yaml: 11
  examples/original.yaml: 12
  status: different values
e:
  examples/comparer.yaml: 12
  examples/original.yaml: 11
  status: different values
x:
  examples/comparer.yaml:
  - c
  - a
  - 1
  - 2
  examples/original.yaml:
  - c
  - a
  - 1
  status: different values
y:
  examples/comparer.yaml:
  - 1
  - 2
  - 3
  examples/original.yaml:
  - 3
  - 2
  - 1
  status: array in different sequence
z:
  examples/comparer.yaml:
  - 3
  - 2
  - '1'
  examples/original.yaml:
  - 3
  - 2
  - 1
  status: different values
```

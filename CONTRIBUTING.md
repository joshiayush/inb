# How to become a contributor and submit your own code

## Contributing A Patch

1. Submit an issue describing your proposed change to the [issue tracker](https://github.com/joshiayush/inb/issues).
2. Please don't mix more than one logical change per submittal, because it makes the history hard to follow. If you want to make a change that doesn't have a corresponding issue in the issue tracker, please create one.
3. Also, coordinate with team members that are listed on the issue in question. This ensures that work isn't being duplicated and communicating your plan early also generally leads to better patches.
4. Fork the repo, develop and test your code changes.
5. Ensure that your code adheres to the existing style. See [.pylintrc](https://github.com/joshiayush/inb/blob/master/.pylintrc) in the root directory.
6. Ensure that your code has an appropriate set of unit tests which all pass.
7. Submit a pull request.

## Style

To keep the source consistent, readable, diffable and easy to merge, we use a fairly rigid coding style, as defined by the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Requirements for Contributors

If you plan to contribute a patch, you need:

- `Python 3.7.12` or `Python 3.7.x` or higher.
- `virtualenv 20.7.2` or `virtualenv 20.7.x` or higher.

## Testing inb

We use [unittest][_unittest] framework for testing, it also comes with a built-in test runner. If you have a python version that is greater than `3.7` then [unittest][_unittest] is already present in your system.

Otherwise install it using the following command,

```shell
pip install unittest
```

To execute all the tests written so far you need to first `cd` into the `inb` directory inside of the project's root directory and then execute the following command to discover and run test cases,

```shell
python3 -m unittest discover -s tests/
```

## Commit

Before commiting please make sure that you have read the [`DEVELOPERS.md`](https://github.com/joshiayush/inb/blob/master/DEVELOPERS.md) file.

## License

By contributing, you agree that your contributions will be licensed under its MIT License. Include the following license at the beginning of every file.

```python
# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
```

<!-- Definitions -->

[_unittest]: https://docs.python.org/3/library/unittest.html

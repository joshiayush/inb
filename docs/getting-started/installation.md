# Installation

## git

```shell
$ git clone https://github.com/JoshiAyush/inb.git inb
$ cd inb
$ sudo ./scripts/rwx.sh
```

Executing script `rwx.sh` will change the directory permissions and will also set the `core.filemode` variable of `git` to `false` so that `git` doesn't track the filemode's if the project is in someone else's computer.

## Dependencies

### Linux

```shell
$ ./scripts/ipackages.sh
```

**Doesn't have Python?**

```shell
$ sudo ./scripts/ipython.sh
```

_Note:_ This will also install the dependencies required to start the development of this project.

### Others

```shell
$ python3.7 -m pip install -r requirements.txt
```

**Doesn't have Python?**

Download it from here [Python][_python].

<!-- Definitions -->

[_python]: https://www.python.org/downloads/

# Installation

## git

```shell
$ git clone https://github.com/JoshiAyush/linkedin-bot.git linkedin-bot
$ cd linkedin-bot
$ sudo ./scripts/rwx.sh
```

Executing script `rwx.sh` will change the directory permissions and will also set the `core.filemode` variable of `git` to `false` so that `git` doesn't track the filemode's if the project is in someone else's computer.

## Dependencies

### Linux

```shell
$ sudo ./scripts/install-dependencies.sh
```

**Doesn't have Python?**

```shell
$ sudo ./scripts/install-python.sh
```

_Note:_ This will also install the dependencies required to start the development of this project.

### Others

```shell
$ pip install selenium

$ pip install webdriver-manager
```

**Doesn't have Python?**

Download it from here [Python][_python].

<!-- Definitions -->

[_python]: https://www.python.org/downloads/

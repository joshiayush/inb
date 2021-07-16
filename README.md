# inb

![](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)

This command line tool is very helpful to increase your connections on **LinkedIn**, you are going to achieve **500+** connections very easily. You just need to run it on your terminal, enter your LinkedIn username and password and execute command `linkedin send`.

## Installation

### git

```shell
$ git clone https://github.com/JoshiAyush/inb.git linkedin-bot
$ cd linkedin-bot
$ sudo ./scripts/rwx.sh
```

Executing script `rwx.sh` will change the directory permissions and will also set the `core.filemode` variable of `git` to `false` so that `git` doesn't track the filemode's if the project is in someone else's computer.

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```shell
$ python3 -m pip3 install -r requirements.txt
```

**Or**

```shell
$ ./scripts/ipackages.sh
```

**Google Chrome Version 91.0.4472.77 (Official Build) (64-bit)** to run chromedriver.

## Available Scripts

In the project directory, you can run:

### `sudo ./scripts/dcache.sh`

Deletes all the cache files that gets created after the program run.

### `./scripts/test.sh`

Tests inb.

#### Check the branch [lvp][_lvp] for a working model of inb

### Happy Hacking

<!-- Definitions -->

[_lvp]: https://github.com/JoshiAyush/inb/tree/lvp

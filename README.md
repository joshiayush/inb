# inb 🤖

This command line tool is very helpful to increase your connections on **LinkedIn**, you are going to achieve **500+** connections
very easily.

## Installation

```shell
$ git clone https://github.com/JoshiAyush/inb.git inb
$ cd inb
```

Executing script `rwx.sh` will change the directory permissions and will also set the `core.filemode` variable of `git` to `false`
so that `git` doesn't track the filemode's if the project is in someone else's computer (only do this if you want to contribute to
`inb` otherwise for just using `inb` you don't really need to do that).

```shell
$ sudo ./scripts/rwx.sh
```

Execute the above command from the project's root directory to change the filemodes.

## Dependencies

You have to install dependencies required for `inb`.

```shell
$ python3 -m pip install requirements.txt
```

Alternatively,

```shell
$ ./scripts/ipackages.sh
```

## inb

Execute the below command from the project's root directory.

```shell
$ python3 inb/inb.py -h
```

You will get a output something like this:

```shell
Usage: inb [-h] {send,config,show,delete,developer} ...

 _     _       _            _ ___         ____        _
| |   (_)_ __ | | _____  __| |_ _|_ __   | __ )  ___ | |_
| |   | | '_ \| |/ / _ \/ _` || || '_ \  |  _ \ / _ \| __|
| |___| | | | |   <  __/ (_| || || | | | | |_) | (_) | |_
|_____|_|_| |_|_|\_\___|\__,_|___|_| |_| |____/ \___/ \__|


LinkedIn Bash, version 1.51.35(1)-release (lbot-1.51.35)
These commands are defined internally. Type '--help' to see this list
Type (command) --help to know more about that command

positional arguments:
  {send,config,show,delete,developer}
                        available actions
    send                sends invitation to people on linkedin.
    config              used to store user's credentials
    show                prints the information that is in the database
    delete              deletes the information stored in the database
    developer           prints the information about the author

optional arguments:
  -h, --help            show this help message and exit
```

You can use the `-h` or `--help` flag with any of the above positional arguments to know more about them.

Look in the [docs][_docs] folder to know more about `inb` and how to use it.

<!-- Definitions -->

[_docs]: https://github.com/JoshiAyush/inb/tree/master/docs

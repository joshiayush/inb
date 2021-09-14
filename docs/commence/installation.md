# Installation

```shell
$ git clone https://github.com/JoshiAyush/inb.git inb
$ cd inb
```

Executing script `rwx.sh` will change the directory permissions and will also set the `core.filemode` variable of `git` to `false`
so that `git` doesn't track the filemode's if the project is in someone else's computer (only do this if you want to contribute to
`inb` otherwise for just using `inb` you don't really need to do that).

```shell
$ sudo ./inb.sh --rwx
```

Execute the above command from the project's root directory to change the filemodes.

## Dependencies

You have to install dependencies required for `inb`.

```shell
$ python3 -m pip install requirements.txt
```

Alternatively,

```shell
$ ./inb.sh --install
```

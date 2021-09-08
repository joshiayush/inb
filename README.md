# inb 🤖

This command line tool is very helpful to increase your connections on **LinkedIn**, you are going to achieve **500+** connections
very easily.

## Features

- [x] Automatically sends invitation to people based on your profile.
- [x] Automatically sends invitation to people based on their industry.
- [x] Automatically sends invitation to people based on their location.
- [x] Automatically sends invitation to people based on their name.
- [x] Automatically connects you with a person based on the profile id.

Know more [here][_project].

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

```
Usage: inb [-h] {send,search,config,show,delete,developer} ...

 _       _
(_)_ __ | |__
| | '_ \| '_ \
| | | | | |_) |
|_|_| |_|_.__/


inb Bash, version 1.51.35(1)-release (inb-1.51.35)
These commands are defined internally. Type '--help' to see this list
Type (command) --help to know more about that command

positional arguments:
  {send,search,config,show,delete,developer}
                        available actions
    send                sends invitation to people on linkedin.
    search              searches people on LinekdIn and then invites them.
    config              used to store user's credentials
    show                prints the information that is in the database
    delete              deletes the information stored in the database
    developer           prints the information about the author

optional arguments:
  -h, --help            show this help message and exit
```

You can use the `-h` or `--help` flag with any of the above positional arguments to know more about them.

### Send Invitation

The `search` command is used to send invitations to people belong to a specific industry.

```shell
$ python3 inb/inb.py -h
```

The above command will give the following output:

```
Usage: inb search [-h] [-e [EMAIL]] [-p [PASSWORD]] [-k [KEYWORD]]
                  [-l [LOCATION]] [-t [TITLE]] [-fn [FIRST_NAME]]
                  [-ln [LAST_NAME]] [-s [SCHOOL]] [-inds [INDUSTRY]]
                  [-cc [CURRENT_COMPANY]] [-pl [PROFILE_LANGUAGE]] [-c] [-i]
                  [-ngpu] [-m]
                  {limit} ...

 _       _
(_)_ __ | |__
| | '_ \| '_ \
| | | | | |_) |
|_|_| |_|_.__/


Searches people on LinkedIn and then invites them.

positional arguments:
  {limit}               available actions
    limit               sets the daily invitation limit

optional arguments:
  -h, --help            show this help message and exit
  -e [EMAIL], --email [EMAIL]
                        User's email address
  -p [PASSWORD], --password [PASSWORD]
                        User's password
  -k [KEYWORD], --keyword [KEYWORD]
                        Keyword to search for
  -l [LOCATION], --location [LOCATION]
                        Location(s) to search in (separated by (:) colon)
  -t [TITLE], --title [TITLE]
                        Match title
  -fn [FIRST_NAME], --first-name [FIRST_NAME]
                        Match first name
  -ln [LAST_NAME], --last-name [LAST_NAME]
                        Match last name
  -s [SCHOOL], --school [SCHOOL]
                        Person's school
  -inds [INDUSTRY], --industry [INDUSTRY]
                        Industry(ies) to search in (separated by (:) colon)
  -cc [CURRENT_COMPANY], --current-company [CURRENT_COMPANY]
                        Person's current company
  -pl [PROFILE_LANGUAGE], --profile-language [PROFILE_LANGUAGE]
                        Person's profile language
  -c, --cookies         uses cookies for authentication
  -i, --incognito       set browser in incognito mode
  -ngpu, --headless     starts chrome in headless mode
  -m, --start-maximized
                        set browser in full screen
```

You target a specific industry by using the `--keyword` flag of `search` command.

```shell
$ python3 inb/inb.py send --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --keyword "Software Developer"
```

The above command will start sending invitation to people who belong to _Software Developer_ industry.

Look in the [docs][_docs] folder to know more about `inb` and how to use it.

<!-- Definitions -->

[_docs]: https://github.com/JoshiAyush/inb/tree/master/docs
[_project]: https://github.com/joshiayush/inb/tree/master/docs/project/README.md

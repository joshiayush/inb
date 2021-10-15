# inb 🤖

You must know the _installation_ guide for `inb` before moving further.

- [Installation][_installation]
- [Testing][_testing]

## inb

- [Overview](#overview)
- [send](#send)

### Overview

Execute the below command from the project's root directory.

```shell
$ python3 inb/inb.py -h
```

You will get the following output:

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

For example:

```shell
$ python3 inb/inb.py send -h
```

The above command will give the following output:

```
Usage: inb send [-h] [-e [EMAIL]] [-p [PASSWORD]] [-c] [-i] [-ngpu] [-m]
                {limit} ...

 _       _     
(_)_ __ | |__  
| | '_ \| '_ \ 
| | | | | |_) |
|_|_| |_|_.__/ 
               

Sends invitation to people on linkedin.

positional arguments:
  {limit}               available actions
    limit               sets the daily invitation limit

optional arguments:
  -h, --help            show this help message and exit
  -e [EMAIL], --email [EMAIL]
                        User's email address
  -p [PASSWORD], --password [PASSWORD]
                        User's password
  -c, --cookies         uses cookies for authentication
  -i, --incognito       set browser in incognito mode
  -ngpu, --headless     starts chrome in headless mode
  -m, --start-maximized
                        set browser in full screen
```

### send

The `send` command is used to send invitations to people on LinkedIn.

```shell
$ python3 inb/inb.py send -h
```

The above command will give the following output:

```
Usage: inb send [-h] [-e [EMAIL]] [-p [PASSWORD]] [-c] [-i] [-ngpu] [-m]
                {limit} ...

 _       _     
(_)_ __ | |__  
| | '_ \| '_ \ 
| | | | | |_) |
|_|_| |_|_.__/ 
               

Sends invitation to people on linkedin.

positional arguments:
  {limit}               available actions
    limit               sets the daily invitation limit

optional arguments:
  -h, --help            show this help message and exit
  -e [EMAIL], --email [EMAIL]
                        User's email address
  -p [PASSWORD], --password [PASSWORD]
                        User's password
  -c, --cookies         uses cookies for authentication
  -i, --incognito       set browser in incognito mode
  -ngpu, --headless     starts chrome in headless mode
  -m, --start-maximized
                        set browser in full screen
```

You can use the `send` command like this:

```shell
$ python3 inb/inb.py send --email "ayush854032@gmail.com" --password "F:(:);GVlk"
```

The above command will send invitations to `40` people on LinkedIn. The reason it sends only `40` invitations because the daily
connection limit is not given.

Set the daily connection limit.

```shell
$ python3 inb/inb.py send --email "ayush854032@gmail.com" --password "F:(:);GVlk" limit 60
```

The above command will send invitations to `60` people on LinkedIn.

The limit must not exceed by `80` otherwise LinkedIn will block you for months. The default connection limit is `40` (recommended),
means if the limit is not given then `inb` will only send invitations upto `40`.

In case, you have a special character in any of your _email_ or _password_ field then you may want to escape it with the character
`(\)`, otherwise it will create problems.

For example:

```shell
$ python3 inb/inb.py send --email "ayush854032@gmail.com" --password "F:(:);GVlk\`"
```

Notice, how I escaped the ```(`)``` character using the `(\)` character. Any kind of escape sequencing will work with `inb`.

Let's talk about flags.

If you want to start sending invitations in `headless` mode, means without opening the browser window then you may want to do this,

```shell
$ python3 inb/inb.py send --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" -ngpu
```

You can either use `-ngpu` or `--headless` both stands for headless mode.

## search

The `search` command is used to send invitations to people belong to a specific industry.

```shell
$ python3 inb/inb.py search -h
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
$ python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --keyword "Software Developer"
```

The above command will start sending invitation to people who belong to _Software Developer_ industry.

The flags applicable in `send` command are also applicable here in `search` command you can use any of those flags. You can also 
specify the `limit` with search command as you did while using the `send` command.

<!-- Definitions -->

[_installation]: https://github.com/JoshiAyush/inb/blob/master/docs/commence/installation.md
[_testing]: https://github.com/JoshiAyush/inb/blob/master/docs/commence/testing.md

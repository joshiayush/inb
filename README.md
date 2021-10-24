# inb 🤖

This command line tool is very helpful to increase your connections on **LinkedIn** by personalizing connection requests.

## Features

- [x] Automatically sends invitation to people based on your profile.
- [x] Automatically sends invitation to people based on their industry.
- [x] Automatically sends invitation to people based on their location.
- [x] Automatically sends invitation to people based on their name.
- [x] Automatically connects you with a person based on the profile id.
- [x] Personalizing connection request messages.

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
$ python3 inb/inb.py search -h
```

The above command will give the following output:

```
Usage: inb search [-h] [-e [EMAIL]] [-p [PASSWORD]] [-k [KEYWORD]]
                  [-l [LOCATION]] [-t [TITLE]] [-fn [FIRST_NAME]]
                  [-ln [LAST_NAME]] [-s [SCHOOL]] [-inds [INDUSTRY]]
                  [-cc [CURRENT_COMPANY]] [-pl [PROFILE_LANGUAGE]]
                  [-msg [MESSAGE] | -tb | -ts | -tre | -tci | -thr | -tiind |
                  -tbfn | -tvc | -tccr] [-f] [--var [VAR]] [-c] [-i] [-ngpu]
                  [-m] [-idb]
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
  -msg [MESSAGE], --message [MESSAGE]
                        adds a message template
  -tb, --template-business
                        template to expand network with business owners
  -ts, --template-sales
                        template to expand network with sales person
  -tre, --template-real-estate
                        template to expand network with real estate agents
  -tci, --template-creative-industry
                        template to expand your network with people who belong
                        to creative industry
  -thr, --template-hr   template to expand your network with HRs
  -tiind, --template-include-industry
                        template to expand your network with people who belong
                        to the industry you specified over command line
  -tbfn, --template-ben-franklin
                        template with subtle pitch
  -tvc, --template-virtual-coffee
                        template to invite people for webinar
  -tccr, --template-common-connection-request
                        template to personalize common connection request
  -f, --force           do not alter the message grammar
  --var [VAR]           template holding your personal details
  -c, --cookies         uses cookies for authentication
  -i, --incognito       set browser in incognito mode
  -ngpu, --headless     starts chrome in headless mode
  -m, --start-maximized
                        set browser in full screen
  -idb, --debug         logs debug info when given
```

You target a specific industry by using the `--keyword` flag of `search` command.

```shell
$ python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --keyword "Software Developer"
```

The above command will start sending invitation to people who belong to _Software Developer_ industry.

## Personalize your request messages

Create a template file name **message.txt** inside folder **inb**.

**message.txt**

```text
TEMPLATE BEGIN:
Hi {{name}},

I'm on a personal mission of expanding my network with like-minded professionals.

If that sounds good, let's connect!
TEMPLATE END;
```

Now use this template to customize your connection request messages.

```shell
$ python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --keyword "Software Developer" --location "United States" --message message.txt
```

**Note: inb will replace the {{name}} with the person name you are sending request to.**

Look in the [docs][_docs] folder to know more about `inb` and how to use it.

<!-- Definitions -->

[_docs]: https://github.com/JoshiAyush/inb/tree/master/docs
[_project]: https://github.com/joshiayush/inb/tree/master/docs/project/README.md

# linkedin-bot's interface

## Built-in CLI

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/>
```

I've made a simple interface for **linkedin-bot** with a very simple logo.

## Commands

### help

If you type `help` some information like the _current release_, _commands_ and some _meta information_ will be printed out.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> help
 LinkedIn Bash, version 1.51.35(1)-release (lnkdbt-1.51.35)
 These commands are defined internally. Type 'help' to see this list.
 Type 'command' --help to know more about that command.

 A ([]) around a command means that the command is optional.
 A (^) next to command means that the command is the default command.
 A (<>) around a name means that the field is required.
 A (/) between commands means that you can write either of these but not all.
 A (*) next to a name means that the command is disabled.

 linkedin [send] [suggestions^] --auto^ [--headless] [--use-cache]
 linkedin [send] [search* industry=example&&location=india+usa+...] --auto^ [--headless] [--use-cache]
 linkedin [invitation-manager*] [show*] --sent*^/--recieved* [--headless] [--use-cache]
 linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless] [--use-cache]
 linkedin [mynetwork*] [show*] [all*^/page > 1^+2+3+...*] [--headless] [--use-cache]
 linkedin [mynetwork*] [sendmessage*] [all*^] [--greet*^] [--headless] [--use-cache]

 config

 show

 delete

 developer

 theme [--parrot^/--normal]

 clear

 exit

 LinkedIn/>
```

### config

Typing `config` alone will print a guide on how to use command `config`.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> config
 config.user.email "example@email.com" --cached
 config.user.password "example@password" --cached
 Or you can use the following command if you don't want to show the password on the screen
 config.user.password --cached (hit enter)
 Password:

 LinkedIn/>
```

**ADDING EMAIL TO CONFIGURATIONS**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> config.user.email "ayush854032@gmail.com"
```

**SAVING EMAIL AS CACHE**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> config.user.email "ayush854032@gmail.com" --cached
```

**ADDING PASSWORD TO CONFIGURATIONS**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> config.user.password "xxx-xxx-xxx"
```

**SAVING PASSWORD AS CACHE**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> config.user.password "xxx-xxx-xxx" --cached
```

### show

This command shows the entered user's configurations.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> show
 ayush854032@gmail.com
 *****************
 Show password anyway? [y/N]: y
 ayush854032@gmail.com
 xxxxx-xxxxx-xxxxx

 LinkedIn/>
```

### delete

This command is used to delete the cache stored as well as the key that was generated to encrypt user fields before storing them as cache.

**DELETING CACHE**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> delete --cache
```

**DELETING KEY**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> delete --key
```

**DELETING KEY AND CACHE**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> delete --cache&&--key
```

## developer

This command will print the information about the author of **linkedin-bot**.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> developer
 Name     :  Ayush Joshi
 Email    :  ayush854032@gmail.com (primary)
 Email    :  joshiayush.joshiayush@gmail.com
 Mobile   :  +91 8941854032 (Only WhatsApp)
 GitHub   :  https://github.com/JoshiAyush
 LinkedIn :  https://www.linkedin.com/in/ayush-joshi-3600a01b7/
```

### theme

This command changes the _theme_ of **linkedin-bot** cli.

**PARROT**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> theme --parrot
```

**NORMAL**

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> theme --normal
```

### clear

This command clears the screen.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> clear
```

### exit

This command exit the cli.

```shell
  _____             _               _              ___         _
 |_   _|           | |             | |            |  _ \      | |
   | |     ^  _ __ | |__  ___   ___| | ^  _ __    | |_) | ___ | |_
   | |    ( )| '_ \|  __`, __`,/  _` |( )| '_ \   |  _ < / _ \| __|
  _| |____( )| | | \ ( _) (__))| (_) #( )| | | \  | |_) | (_) | |_
 |________(_)|_| |_|_|  \\____ \___/_|(_)| | | |  |____/ \___/ \__|

 Type help for more information!

 LinkedIn/> exit
```

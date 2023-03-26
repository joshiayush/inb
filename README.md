<div id="top"></div>

<div align="center">
  <a href="https://github.com/joshiayush/inb">
    <img src="./media/linkedin.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">inb</h3>

  <p align="center">
    Automatically connect to over <strong>900 million</strong> professionals on LinkedIn!
    <br />
    <a href="https://github.com/joshiayush/inb/tree/master/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/joshiayush/inb/wiki">Wiki</a>
    ·
    <a href="https://github.com/joshiayush/inb/issues">Report Bug</a>
    ·
    <a href="https://github.com/joshiayush/inb/issues">Request Feature</a>
  </p>
</div>

**inb** is an automation tool for LinkedIn that allows users to automate various tasks, such as sending connection requests, messaging connections, and endorsing skills. With **inb**, users can save time and streamline their LinkedIn outreach efforts.

The tool is written in Python and uses the **LinkedIn Voyager API** to interact with LinkedIn.

**inb** is designed for professionals who want to expand their network and increase their visibility on LinkedIn. It can be used for personal or business purposes, and is ideal for individuals who want to grow their network without spending hours manually sending connection requests and messages.

The tool is open source and available on GitHub, so users can contribute to the development of the project and customize it to their specific needs. To get started, simply download the tool from GitHub and follow the instructions in the **`README`** file.

> No **"official"** API access required - Just use a valid LinkedIn account!

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Clone

Clone the repository.

```shell
git clone https://github.com/joshiayush/inb.git
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Docker usage

To use the app with docker, you can use the following command:

```shell
docker build -t inb . && docker run -it inb search --email ayush854032@gmail.com --password xxx-xxx-xxx \
  --keyword 'Software Engineer'
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Installation

Next step is to install all the dependencies required for project **inb** listed in the `requirements.txt` file.

```shell
python3 -m pip install [-r] requirements.txt
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Usage

To send invitations to people on LinkedIn you could use:

```shell
./inb/inb.py search --email ayush854032@gmail.com --password xxx-xxx-xxx \
  --keyword 'Software Engineer'
```

A quick usage guide:

```
Usage: inb.py search [OPTIONS]

   Searches for the specific keyword given and sends invitation to them.

  Usage:

    ./inb/inb.py search --email "username" --password "password"
      --keyword "Software developer"

  inb supports cookie based authentication - use --refresh-cookies in case
  you encounter error LinkedInSessionExpiredException.

    ./inb/inb.py search --email "username" --password "password"
      --keyword "Software developer" --refersh-cookies

  Also, for security purpose you can omit the --pasword argument over the
  command-line and later on executing the tool you'll be prompted to enter
  your password which will be hidden even after pressing keystrokes.

    ./inb/inb.py search --email "username" --keyword "Software developer"
      --refersh-cookies

Options:
  --email TEXT              LinkedIn username.  [required]
  --password TEXT           LinkedIn password.  [required]
  --keyword TEXT            Keyword to search for.  [required]
  --regions LIST            Search people based on these regions.
  --connection-of TEXT      Profile id for mutual connection.
  --network_depths LIST     Network depths to dig into.
  --network-depth TEXT      Network depth to dig into.
  --industries LIST         Search people from these industries.
  --current-company TEXT    Search people working at this company.
  --profile-languages LIST  Person profile languages.
  --schools LIST            Search for profiles mentioning this school.
  --refresh-cookies         Update cookies if given.
  --limit INTEGER           Number of invitations to send.
  --debug                   Prints out debugging information at runtime.
  --help                    Show this message and exit.
```

> **Any problems encountered in non-linux environment should be reported immediately before passing comments on the portability of this tool as I've only built and tested it on Linux!**

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Contribution

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement", "bug", or "documentation". Don't forget to give the project a star! Thanks again!

Project [**inb**][_inb] is hosted on [GitHub][_github]. If you want to contribute changes please make sure to read the [`CONTRIBUTING.md`][_inb_contrib_f] file. You can also contribute changes to the [`CONTRIBUTING.md`][_inb_contrib_f] file itself.

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

<!-- Definitions -->

[_github]: https://www.github.com
[_inb]: https://www.github.com/joshiayush/inb

<!-- Attached links -->

[back_to_top]: https://img.shields.io/badge/-Back%20to%20top-lightgrey

<!-- Files -->

[_inb_contrib_f]: https://github.com/joshiayush/inb/blob/master/CONTRIBUTING.md

<div id="top"></div>

<div align="center">

[![Contributors][inb_contributors]][inb_contributors_url]
[![Forks][inb_forks]][inb_forks_url]
[![Stargazers][inb_stars]][inb_stars_url]
[![Issues][inb_issues]][inb_issues_url]
[![LICENSE][inb_license]][inb_license_url]
[![LinkedIn][developer_linkedin]][developer_linkedin_url]

</div>

<br />
<div align="center">
  <a href="https://github.com/joshiayush/inb">
    <img src="./media/linkedin.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">inb</h3>

  <p align="center">
    Automate the world of LinkedIn!
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

<details>
  <summary>Contents</summary>
  <ol>
    <li>
      <a href="#inb">inb</a>
      <ul>
        <li><a href="#technologies-used">Technologies Used</li>
      </ul>
    </li>
    <li>
      <a href="#commence">Commence</a>
      <ul>
        <li>
          <a href="#prerequisites">Prerequisites</a>
          <ul>
            <li><a href="#ubuntu">Ubuntu</a></li>
          </ul>
        </li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contribution">Contribution</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#developers">Developers</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#maintainership">Maintainership</a></li>
  </ol>
</details>

# inb

![inb](./media/inb.gif)

Word **inb** is made up of two words "**in**" and "**b**" where "**in**" stands for [LinkedIn][_linkedin] which is an _American business and employment-oriented online service that operates via websites and mobile apps_ and "**b**" stands for bot. So by now you've already deduced that inb is a bot that automates [LinkedIn][_linkedin].

**Features include:**

- Automatically send invitation to people in your MyNetwork page.
- Automatically send invitation to people based on their industry, location, name and profile id.
- Personalize connection request messages.

**Features planned to include:**

- Automatically remove connections.
- [Information Gathering][_inb_info_gathering_issue] module to gather information of a person or a company on LinkedIn

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## Technologies Used

<div align="center">

![Bash][bash]
![Python][python]
![Python Selenium][python_selenium]
![Chromedriver][chromedriver]

</div>

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Commence

To get a local copy up and running follow the steps below.

## Prerequisites

You must have a `Python 3.7.x` version or higher. We recommend setting up a virtual environment using `virtualenv`.

### Ubuntu

**Step 1: Install Virtualenv**

First, we will update our `apt`, then we will install the **virtualenv** module.

```shell
sudo apt update
sudo apt install python-virtualenv
```

**Step 2: Create a Virtual Environment & Install Python 3**

Virtualenv works by creating a folder that houses the necessary Python executables in the bin directory. In this instance, we are
installing `Python 3.7.12` while setting up the virtual environment in the project's directory.

```shell
virtualenv -p /usr/bin/python3 .
```

<p align="right"><a href="#virtualenv_imp_note">Important note!</a></p>

**Step 3: Activate Your Virtual Environment**

From the project's root directory execute the following command.

```shell
source bin/activate
```

<p align="right"><a href="#virtualenv_imp_note">Important note!</a></p>

<div id="virtualenv_imp_note">
  <strong>Note: Virtual environment setup and activation step should be done after cloning the repository.</strong>
</div>

<!-- @TODO(@): Add installation steps for Windows and MacOS. -->

## Installation

Clone the repository.

```shell
git clone https://github.com/joshiayush/inb.git
```

Next step is to install all the dependencies required for project **inb** listed in the `requirements.txt` file.

```shell
python3 -m pip install [-r] requirements.txt
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Usage

To send invitations to people on LinkedIn you must execute the following command. The following command will send invitations to 20 people that are in your `MyNetwork` page.

```
python3 inb/inb.py send --email ayush854032@gmail.com --password xxx-xxx-xxx
```

Go to our [Wiki][_inb_wiki] for more usage instructions.

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Contribution

Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement", "bug", or "documentation". Don't forget to give the project a star! Thanks again!

Project [**inb**][_inb] is hosted on [GitHub][_github]. If you want to contribute changes please make sure to read the [`CONTRIBUTING.md`][_inb_contrib_f] file. You can also contribute changes to the [`CONTRIBUTING.md`][_inb_contrib_f] file itself.

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# License

Distributed under the MIT License. See [`LICENSE`][_inb_license_f] for more information. Please do not use project [**inb**][_inb] if you have any issue with MIT License.

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Developers

- [**joshiayush**](https://www.github.com/joshiayush)

  <a href="https://github.com/joshiayush">
  <img src="./media/github.png" alt="Logo" width="40" height="40">
  </a>
  <a href="https://www.linkedin.com/in/ayush-joshi-3600a01b7/">
  <img src="./media/linkedin.png" alt="Logo" width="40" height="40">
  </a>
  <a href="http://twitter.com/joshiayushjoshi">
  <img src="./media/twitter.png" alt="Logo" width="40" height="40">
  </a>
  <a href="https://stackoverflow.com/users/13910122/ayush">
  <img src="./media/stack-overflow.png" alt="Logo" width="40" height="40">
  </a>

<!-- Contibutors who have contributed non-trivial changes are encouraged to add their details here. -->

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Acknowledgments

A big thanks goes to the following resources who have helped in the development of project [**inb**][_inb].

- [Flaticon](https://www.flaticon.com/)
- [Shields.io](https://shields.io/)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Selenium With Python](https://selenium-python.readthedocs.io/)
- [Stack Overflow](https://www.stackoverflow.com)

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

# Maintainership

We're actively seeking maintainers that will triage issues and pull requests and cut releases. If you are interested in maintaining project [**inb**][_inb], send an email to ayush854032@gmail.com with a subject "**Interested in maintaining project inb**".

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

<!-- Definitions -->

[_github]: https://www.github.com
[_linkedin]: https://www.linkedin.com
[_inb]: https://www.github.com/joshiayush/inb

<!-- Shields and attached links -->

[inb_contributors]: https://img.shields.io/github/contributors/joshiayush/inb?logo=GitHub&style=for-the-badge
[inb_contributors_url]: https://github.com/joshiayush/inb/graphs/contributors
[inb_forks]: https://img.shields.io/github/forks/joshiayush/inb?logo=GitHub&style=for-the-badge
[inb_forks_url]: https://github.com/joshiayush/inb/network/members
[inb_stars]: https://img.shields.io/github/stars/joshiayush/inb?logo=GitHub&style=for-the-badge
[inb_stars_url]: https://github.com/joshiayush/inb/stargazers
[inb_issues]: https://img.shields.io/github/issues/joshiayush/inb?logo=GitHub&style=for-the-badge
[inb_issues_url]: https://github.com/joshiayush/inb/issues
[inb_license]: https://img.shields.io/github/license/joshiayush/inb?logo=GitHub&style=for-the-badge
[inb_license_url]: https://github.com/joshiayush/inb/blob/master/LICENSE
[developer_linkedin]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[developer_linkedin_url]: https://www.linkedin.com/in/ayush-joshi-3600a01b7/
[back_to_top]: https://img.shields.io/badge/-Back%20to%20top-lightgrey

<!-- Technologies used -->

[bash]: https://img.shields.io/badge/-Bash-blue?style=for-the-badge
[python]: https://img.shields.io/badge/-Python-blue?style=for-the-badge
[python_selenium]: https://img.shields.io/badge/-Python%20Selenium-blue?style=for-the-badge
[chromedriver]: https://img.shields.io/badge/-Chromedriver-blue?style=for-the-badge

<!-- Issues -->

[_inb_info_gathering_issue]: https://github.com/joshiayush/inb/issues/16

<!-- Wiki -->

[_inb_wiki]: https://github.com/joshiayush/inb/wiki

<!-- Files -->

[_inb_contrib_f]: https://github.com/joshiayush/inb/blob/master/CONTRIBUTING.md
[_inb_license_f]: https://github.com/joshiayush/inb/blob/master/LICENSE

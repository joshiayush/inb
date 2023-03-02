<div id="top"></div>

# Style Guide

Use a consistent coding style provided by [Google Python Style guide](https://google.github.io/styleguide/pyguide.html) which I recommend reading because they also provide information on how to disable [pylint][_pylint] if that's a requirement.

## [`yapf`][_yapf]

In order to be consistent with the rest of the coding style use [`yapf`][_yapf] (A Google Python code formatter).

### Installation

```shell
python3 -m pip install yapf
```

### Settings

Use the following settings to configure [`yapf`][_yapf] for your workspace in [vscode](https://code.visualstudio.com/).

```json
{
  "python.formatting.provider": "yapf",
  "python.formatting.yapfArgs": [
    "--style={based_on_style: google, column_limit: 80, indent_width: 2}"
  ]
}
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

## [`pylint`][_pylint]

In addition to [`yapf`][_yapf] also install [`pylint`][_pylint] to find out bugs in your code, check the quality of your code and more.

### Installation

```shell
python3 -m pip install pylint
```

### Settings

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintPath": "pylint",
  "python.linting.pylintEnabled": true
}
```

<div align="right">
  <a href="#top">
  
  ![Back to top][back_to_top]
  
  </a>
</div>

<!-- Definitions -->

[_yapf]: https://github.com/google/yapf
[_pylint]: https://pypi.org/project/pylint/

<!-- Shields -->

[back_to_top]: https://img.shields.io/badge/-Back%20to%20top-lightgrey

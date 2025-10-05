# Tutorial

> **Note:** Did you find any of these instructions confusing? [Edit this file](https://github.com/AlonKellner/cookiecutter-pyproject-2025/blob/master/docs/tutorial.md) and submit a pull request with your improvements!

To start with, you will need a [GitHub account](https://github.com/). Create it before you get started on this tutorial. If you are new to Git and GitHub, you should probably spend a few minutes on some of the tutorials at the top of the page at [GitHub Help](https://help.github.com/).

## Step 1: Install Cookiecutter

First, you need to create and activate a virtualenv for the project. Use your favorite method, or create a virtualenv for your new project like this:

```bash
virtualenv ~/.virtualenvs/myproject
```

Here, `myproject` is the name of the project that you'll create.

Activate your environment:

```bash
source bin/activate
```

On Windows, activate it like this. You may find that using a Command Prompt window works better than gitbash.

```powershell
> \path\to\env\Scripts\activate
```

> **Note:** If you create your virtual environment folder in a different location within your project folder, be sure to add that path to your .gitignore file.

Install cookiecutter:

```bash
pip install cookiecutter
```

## Step 2: Generate Your Project

Now it's time to generate your Python project.

Use cookiecutter, pointing it at the cookiecutter-pyproject-2025 repo:

```bash
cookiecutter https://github.com/AlonKellner/cookiecutter-pyproject-2025.git
```
